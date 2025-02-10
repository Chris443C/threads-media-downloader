import json
import requests
import os

# Load detected threats
with open("detected_threats.json", "r") as file:
    threats = json.load(file)

if threats:
    alert_message = f"🚨 Incident Response: {len(threats)} security threats detected!\n"

    for threat in threats:
        alert_message += f"🔴 IP: {threat['ip_address']} | Failed Logins: {threat['failed_logins']} | API Requests: {threat['api_requests']}\n"

        # Auto-block IP using Cloudflare API
        cloudflare_api_url = "https://api.cloudflare.com/client/v4/user/firewall/rules"
        cloudflare_payload = {
            "mode": "block",
            "configuration": {"target": "ip", "value": threat["ip_address"]},
            "notes": "AI Auto-Blocked Threat"
        }
        headers = {"Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}"}
        requests.post(cloudflare_api_url, json=cloudflare_payload, headers=headers)

    # Send Alert to Slack
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(slack_url, json={"text": alert_message})

    # Send Alert to PagerDuty
    pagerduty_url = "https://events.pagerduty.com/v2/enqueue"
    pagerduty_payload = {
        "routing_key": os.getenv("PAGERDUTY_API_KEY"),
        "event_action": "trigger",
        "payload": {
            "summary": alert_message,
            "severity": "critical",
            "source": "AI Incident Response",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 AI blocked threats & notified security teams!")
else:
    print("✅ No immediate threats detected.")

import json
import requests
import os

# Load correlated threats
with open("correlated_threats.json", "r") as file:
    threats = json.load(file)

if threats:
    alert_message = f"🚨 Active Threat Alert: {len(threats)} internal threats match external intelligence!\n"

    for threat in threats:
        alert_message += f"🔥 IP: {threat['ip_address']} | Event: {threat['event_type']} | Time: {threat['timestamp']}\n"

    # Send Alert to Slack
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(slack_url, json={"text": alert_message})

    # Send Alert to PagerDuty for immediate action
    pagerduty_url = "https://events.pagerduty.com/v2/enqueue"
    pagerduty_payload = {
        "routing_key": os.getenv("PAGERDUTY_API_KEY"),
        "event_action": "trigger",
        "payload": {
            "summary": alert_message,
            "severity": "critical",
            "source": "AI Threat Intelligence",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 Active threats escalated to security teams!")
else:
    print("✅ No active threats detected.")

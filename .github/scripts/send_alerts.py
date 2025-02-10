import json
import requests
import os

# Load detected anomalies
with open("anomalies.json", "r") as file:
    anomalies = json.load(file)

if anomalies:
    alert_message = f"🚨 Security Alert: {len(anomalies)} anomalies detected!\n"

    for anomaly in anomalies:
        alert_message += f"🕵️ IP: {anomaly['ip']} | Action: {anomaly['action']}\n"

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
            "source": "AI Anomaly Detector",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 Alerts sent to Slack & PagerDuty!")
else:
    print("✅ No anomalies detected.")

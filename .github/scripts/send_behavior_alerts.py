import json
import requests
import os

# Load user behavior anomalies
with open("behavior_anomalies.json", "r") as file:
    anomalies = json.load(file)

if anomalies:
    alert_message = f"🚨 User Behavior Alert: {len(anomalies)} suspicious activities detected!\n"

    for anomaly in anomalies:
        alert_message += f"🕵️ User ID: {anomaly['user_id']} | Transactions: {anomaly['transactions']} | API Requests: {anomaly['api_requests']}\n"

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
            "source": "AI Behavioral Analytics",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 User behavior alerts sent to Slack & PagerDuty!")
else:
    print("✅ No unusual behavior detected.")

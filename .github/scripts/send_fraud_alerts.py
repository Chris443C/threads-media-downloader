import json
import requests
import os

# Load fraud cases
with open("fraud_cases.json", "r") as file:
    fraud_cases = json.load(file)

if fraud_cases:
    alert_message = f"🚨 Fraud Alert: {len(fraud_cases)} suspicious activities detected!\n"

    for fraud in fraud_cases:
        alert_message += f"🔍 User: {fraud['user_id']} | Location: {fraud['location']} | Amount: ${fraud['transaction_amount']}\n"

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
            "source": "AI Fraud Detector",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 Fraud alerts sent to Slack & PagerDuty!")
else:
    print("✅ No fraud detected.")

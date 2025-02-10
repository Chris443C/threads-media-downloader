import json
import requests
import os

# Load fraud risk predictions
with open("fraud_predictions.json", "r") as file:
    fraud_predictions = json.load(file)

# Filter high-risk transactions (Risk > 0.8)
high_risk = [f for f in fraud_predictions if f["fraud_risk"] > 0.8]

if high_risk:
    alert_message = f"🚨 Fraud Risk Alert: {len(high_risk)} high-risk transactions detected!\n"

    for fraud in high_risk:
        alert_message += f"⚠️ Amount: ${fraud['transaction_amount']} | Risk Score: {fraud['fraud_risk']:.2f}\n"

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
            "source": "AI Fraud Prediction",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 Fraud risk alerts sent to Slack & PagerDuty!")
else:
    print("✅ No high-risk transactions detected.")

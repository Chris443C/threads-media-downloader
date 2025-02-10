import json
import requests
import os

# Load risk scores
with open("risk_scores.json", "r") as file:
    risk_scores = json.load(file)

# Filter high-risk threats (Risk Score > 80)
high_risk = [event for event in risk_scores if event["risk_score"] > 80]

if high_risk:
    alert_message = f"🚨 High-Risk Security Alert: {len(high_risk)} critical incidents detected!\n"

    for event in high_risk:
        alert_message += f"🔥 Event: {event['event_type']} | Severity: {event['severity']} | Risk Score: {event['risk_score']:.2f}\n"

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
            "source": "AI Risk Scoring",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 High-Risk Threats Escalated to Security Teams!")
else:
    print("✅ No critical threats detected.")

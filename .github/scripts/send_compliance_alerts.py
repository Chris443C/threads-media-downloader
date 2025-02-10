import json
import requests
import os

# Load compliance violations
with open("compliance_violations.json", "r") as file:
    violations = json.load(file)

if violations:
    alert_message = f"🚨 Compliance Violation Alert: {len(violations)} issues detected!\n"

    for violation in violations:
        alert_message += f"📌 {violation['standard']} - {violation['policy']} (Expected: {violation['expected']}, Found: {violation['actual']})\n"

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
            "severity": "high",
            "source": "AI Compliance Checker",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("🚨 Compliance violation alerts sent to Slack & PagerDuty!")
else:
    print("✅ System is fully compliant!")

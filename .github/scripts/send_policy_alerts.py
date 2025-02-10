import json
import requests
import os

# Load applied policy fixes
with open("compliance_violations.json", "r") as file:
    violations = json.load(file)

if violations:
    alert_message = f"🔧 Security Policy Fixes Applied: {len(violations)} issues resolved!\n"

    for violation in violations:
        alert_message += f"✅ {violation['standard']} - {violation['policy']} now set to {violation['expected']}\n"

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
            "severity": "info",
            "source": "AI Security Policy Automation",
        }
    }
    requests.post(pagerduty_url, json=pagerduty_payload)

    print("✅ Security policy updates sent to Slack & PagerDuty!")
else:
    print("🚀 No fixes needed, system is already compliant!")

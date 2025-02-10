import json
import requests
import os

# Load security recommendations
with open("security_recommendations.json", "r") as file:
    recommendations = json.load(file)

# Notify users via email or API (Simulated)
for rec in recommendations:
    user_id = rec["user_id"]
    message = rec["recommendation"]

    # Send Email Notification (Simulated)
    email_api_url = os.getenv("EMAIL_API_URL")
    email_payload = {
        "to": f"user{user_id}@example.com",
        "subject": "Security Alert: Account Risk Assessment",
        "body": message
    }
    requests.post(email_api_url, json=email_payload)

    print(f"📩 Sent Security Recommendation to User {user_id}")

# Send Summary to Slack
slack_url = os.getenv("SLACK_WEBHOOK_URL")
requests.post(slack_url, json={"text": f"📢 AI Sent {len(recommendations)} Security Recommendations to Users!"})

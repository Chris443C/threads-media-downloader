import openai
import os
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

# Simulated user security data
user_data = pd.DataFrame({
    "user_id": np.arange(1, 101),
    "failed_logins": np.random.randint(0, 10, 100),
    "password_age_days": np.random.randint(0, 365, 100),
    "multi_factor_enabled": np.random.choice([0, 1], size=100, p=[0.6, 0.4]),
    "security_risk": np.random.uniform(0, 1, 100)
})

# Define risk thresholds
HIGH_RISK_THRESHOLD = 0.75
MEDIUM_RISK_THRESHOLD = 0.50

# Generate security recommendations
recommendations = []
for _, row in user_data.iterrows():
    user_id = row["user_id"]
    risk_score = row["security_risk"]
    failed_logins = row["failed_logins"]
    password_age = row["password_age_days"]
    mfa_enabled = row["multi_factor_enabled"]

    if risk_score > HIGH_RISK_THRESHOLD:
        recommendation = f"User {user_id}: 🚨 HIGH RISK! Enable multi-factor authentication and reset your password immediately."
    elif risk_score > MEDIUM_RISK_THRESHOLD:
        recommendation = f"User {user_id}: ⚠️ MEDIUM RISK! Consider enabling multi-factor authentication."
    else:
        recommendation = f"User {user_id}: ✅ LOW RISK. Keep your account secure by updating your password regularly."

    recommendations.append({"user_id": user_id, "recommendation": recommendation})

# Save recommendations for notifications
with open("security_recommendations.json", "w") as f:
    json.dump(recommendations, f, indent=4)

print(f"✅ AI Generated Security Recommendations for {len(user_data)} users!")

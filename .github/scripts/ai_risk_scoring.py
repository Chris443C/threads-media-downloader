import openai
import os
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# Simulated security event data (normally pulled from logs)
security_events = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(days=7), periods=500, freq="H"),
    "event_id": np.arange(500),
    "event_type": np.random.choice(["DDoS", "Brute Force", "Malware", "Phishing", "Insider Threat"], 500),
    "severity": np.random.randint(1, 10, 500),  # 1 = Low, 10 = High
    "affected_users": np.random.randint(1, 500, 500),
    "data_exfiltrated_mb": np.random.uniform(0, 500, 500)
})

# Define risk scoring model inputs
X = security_events[["severity", "affected_users", "data_exfiltrated_mb"]].values
y = security_events["severity"] + (security_events["affected_users"] * 0.1) + (security_events["data_exfiltrated_mb"] * 0.05)

# Train AI-based risk scoring model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict risk scores
security_events["risk_score"] = model.predict(X)

# Categorize risk levels
security_events["risk_level"] = pd.cut(
    security_events["risk_score"],
    bins=[0, 30, 60, 100],
    labels=["Low", "Medium", "High"]
)

# Save risk assessment results
security_events.to_json("risk_scores.json", orient="records")

# Generate risk distribution report
import matplotlib.pyplot as plt

plt.hist(security_events["risk_score"], bins=20, color="red", alpha=0.7)
plt.xlabel("Risk Score")
plt.ylabel("Number of Incidents")
plt.title("Security Risk Distribution")
plt.savefig("risk_score_report.png")

print(f"✅ AI Generated Risk Scores for {len(security_events)} security events!")

import openai
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

# Simulated user activity data (normally pulled from logs or a database)
user_activity = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(days=30), periods=1000, freq="H"),
    "user_id": np.random.randint(1, 200, 1000),
    "transactions": np.random.randint(0, 10, 1000),
    "failed_logins": np.random.randint(0, 5, 1000),
    "api_requests": np.random.randint(50, 500, 1000)
})

# Train AI-based anomaly detection model
X = user_activity[["transactions", "failed_logins", "api_requests"]].values
model = IsolationForest(contamination=0.02, random_state=42)
user_activity["anomaly"] = model.fit_predict(X)

# Identify anomalous behavior
anomalies = user_activity[user_activity["anomaly"] == -1]

# Save anomalies to a JSON file for alerting
anomalies.to_json("behavior_anomalies.json", orient="records")

# Generate Behavioral Analytics Report
plt.scatter(user_activity["transactions"], user_activity["api_requests"], c=user_activity["anomaly"], cmap="coolwarm")
plt.xlabel("Transactions")
plt.ylabel("API Requests")
plt.title("User Behavior Analysis")
plt.savefig("behavior_analysis_report.png")

print(f"✅ AI Identified {len(anomalies)} unusual user behavior patterns!")

import openai
import os
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# Simulated real-time log data (normally pulled from a SIEM or logs)
logs = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(hours=6), periods=500, freq="1min"),
    "ip_address": ["192.168.1." + str(i % 255) for i in range(500)],
    "failed_logins": np.random.randint(0, 10, 500),
    "api_requests": np.random.randint(50, 1000, 500),
    "data_transferred_mb": np.random.uniform(0.1, 500, 500)
})

# AI-based anomaly detection (Isolation Forest)
X = logs[["failed_logins", "api_requests", "data_transferred_mb"]].values
model = IsolationForest(contamination=0.02, random_state=42)
logs["threat"] = model.fit_predict(X)

# Identify threats
threats = logs[logs["threat"] == -1]

# Save detected threats for mitigation
threats.to_json("detected_threats.json", orient="records")

print(f"✅ AI Detected {len(threats)} potential security threats!")

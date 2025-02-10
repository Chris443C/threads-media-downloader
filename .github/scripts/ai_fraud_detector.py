import openai
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import json

# Simulated transaction & login data (normally from a database or API)
user_logs = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(days=7), periods=100, freq="H"),
    "user_id": np.random.randint(1, 50, 100),
    "transaction_amount": np.random.randint(10, 500, 100),
    "location": np.random.choice(["USA", "Germany", "China", "Russia", "Brazil"], 100),
    "login_attempts": np.random.randint(1, 5, 100)
})

# AI-based Fraud Detection Model (Isolation Forest)
X = user_logs[["transaction_amount", "login_attempts"]].values
model = IsolationForest(contamination=0.05, random_state=42)
user_logs["fraud"] = model.fit_predict(X)

# Identify fraud cases
fraud_cases = user_logs[user_logs["fraud"] == -1]

# Save fraud cases for alerting
fraud_cases.to_json("fraud_cases.json", orient="records")

print(f"✅ Detected {len(fraud_cases)} suspicious transactions & logins!")

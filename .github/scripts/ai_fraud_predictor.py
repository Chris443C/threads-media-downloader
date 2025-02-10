import openai
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

# Simulated historical fraud data (normally fetched from a database)
user_data = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(days=30), periods=500, freq="H"),
    "user_id": np.random.randint(1, 100, 500),
    "transaction_amount": np.random.randint(10, 1000, 500),
    "login_attempts": np.random.randint(1, 10, 500),
    "fraud": np.random.choice([0, 1], size=500, p=[0.9, 0.1])  # 10% fraud cases
})

# Define training features & target
X = user_data[["transaction_amount", "login_attempts"]]
y = user_data["fraud"]

# Train AI-based fraud prediction model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict fraud risk for new transactions
new_data = pd.DataFrame({
    "transaction_amount": np.random.randint(10, 1000, 10),
    "login_attempts": np.random.randint(1, 10, 10)
})
new_data["fraud_risk"] = model.predict_proba(new_data)[:, 1]  # Get fraud probability

# Save risk predictions
new_data.to_json("fraud_predictions.json", orient="records")

# Generate Fraud Risk Report
plt.hist(new_data["fraud_risk"], bins=10, color="red", alpha=0.7)
plt.xlabel("Fraud Risk Score")
plt.ylabel("Number of Transactions")
plt.title("Fraud Risk Distribution")
plt.savefig("fraud_risk_report.png")

print(f"✅ AI Predicted Fraud Risk for {len(new_data)} transactions!")

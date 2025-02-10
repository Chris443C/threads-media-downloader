import openai
import os
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# Connect to Elasticsearch (Kibana Logs)
es = Elasticsearch(["http://elasticsearch:9200"])

# Retrieve logs from the last 24 hours
query = {
    "query": {
        "range": {
            "@timestamp": {
                "gte": "now-24h/h",
                "lt": "now/h"
            }
        }
    }
}

logs = es.search(index="logs-*", body=query, size=1000)

# Process logs into DataFrame
data = []
for log in logs["hits"]["hits"]:
    source = log["_source"]
    data.append([source["timestamp"], source["ip"], source["action"]])

df = pd.DataFrame(data, columns=["timestamp", "ip", "action"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Convert actions into numerical values
df["action_encoded"] = df["action"].astype("category").cat.codes

# Train an AI-based anomaly detector (Isolation Forest)
X = df[["action_encoded"]].values
model = IsolationForest(contamination=0.02, random_state=42)
df["anomaly"] = model.fit_predict(X)

# Identify anomalies
anomalies = df[df["anomaly"] == -1]

# Save anomalies to a JSON file for alerting
anomalies.to_json("anomalies.json", orient="records")

print(f"✅ Detected {len(anomalies)} suspicious activities!")

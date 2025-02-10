import openai
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Load historical scaling data (simulated for now)
history = pd.DataFrame({
    "timestamp": pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq="D"),
    "cpu_usage": [40, 55, 65, 80, 75, 60, 50],
    "replica_count": [2, 3, 4, 6, 5, 4, 3]
})

# Train an AI Model (Linear Regression) to predict scaling needs
X = np.array(history["cpu_usage"]).reshape(-1, 1)
y = np.array(history["replica_count"])
model = LinearRegression()
model.fit(X, y)

# Predict the optimal scaling for the next hour
predicted_cpu = np.random.randint(50, 90)  # Simulated CPU usage
predicted_replicas = int(round(model.predict([[predicted_cpu]])[0]))

# Ensure replicas stay within bounds
predicted_replicas = max(2, min(predicted_replicas, 10))

# Generate a new HPA configuration
hpa_yaml = f"""
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: threads-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: threads-downloader
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {predicted_cpu}
"""

# Save AI-generated HPA configuration
with open("k8s/hpa.yaml", "w") as f:
    f.write(hpa_yaml)

print(f"✅ AI Predicted Scaling: {predicted_replicas} Replicas for {predicted_cpu}% CPU Usage")

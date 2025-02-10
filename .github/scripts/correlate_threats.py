import json
import pandas as pd

# Load external threat intelligence data
with open("threat_intelligence.json", "r") as file:
    threat_intel = json.load(file)

# Load internal security logs (simulated)
internal_logs = pd.DataFrame({
    "ip_address": ["192.168.1.100", "185.220.101.45", "37.120.145.234"],
    "event_type": ["Brute Force", "DDoS", "Malware"],
    "timestamp": pd.to_datetime(["2024-02-09 12:00", "2024-02-09 13:00", "2024-02-09 14:00"])
})

# Extract blacklisted IPs from threat intelligence
blacklisted_ips = []
for source, data in threat_intel.items():
    if isinstance(data, dict) and "results" in data:
        blacklisted_ips.extend([entry.get("ip") for entry in data["results"] if entry.get("ip")])

# Identify matches between external threat intel and internal logs
correlated_threats = internal_logs[internal_logs["ip_address"].isin(blacklisted_ips)]

# Save correlated threats
correlated_threats.to_json("correlated_threats.json", orient="records")

print(f"✅ Found {len(correlated_threats)} internal threats matching external intelligence!")

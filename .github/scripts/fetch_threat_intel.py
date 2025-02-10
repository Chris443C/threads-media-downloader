import requests
import json
import os

# Define external threat intelligence sources
threat_feeds = {
    "AlienVault OTX": "https://otx.alienvault.com/api/v1/pulses/subscribed",
    "AbuseIPDB": "https://api.abuseipdb.com/api/v2/blacklist",
    "Cyber Threat Alliance": "https://www.cyberthreatalliance.org/api/threat-feed",
}

# Fetch threat intelligence data
threat_data = {}
headers = {
    "X-OTX-API-KEY": os.getenv("ALIENVAULT_API_KEY"),
    "Key": os.getenv("ABUSEIPDB_API_KEY")
}

for source, url in threat_feeds.items():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            threat_data[source] = response.json()
        else:
            print(f"⚠️ Failed to fetch data from {source}")
    except Exception as e:
        print(f"❌ Error fetching {source}: {e}")

# Save threat intelligence data
with open("threat_intelligence.json", "w") as f:
    json.dump(threat_data, f, indent=4)

print(f"✅ Fetched Threat Intelligence from {len(threat_data)} sources!")

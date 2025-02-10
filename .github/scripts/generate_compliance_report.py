import json
import pandas as pd

# Load compliance violations
with open("compliance_violations.json", "r") as file:
    violations = json.load(file)

# Convert to DataFrame & Save as Report
df = pd.DataFrame(violations)
df.to_csv("compliance_report.csv", index=False)

print("📜 Compliance Report Generated!")

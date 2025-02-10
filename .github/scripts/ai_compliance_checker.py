import openai
import os
import pandas as pd
import json

# Define security policies
security_policies = {
    "PCI DSS": {
        "password_expiration_days": 90,
        "multi_factor_required": True,
        "logs_retention_days": 365
    },
    "GDPR": {
        "data_encryption": True,
        "user_consent_required": True,
        "right_to_erasure_enabled": True
    },
    "SOC 2": {
        "access_control_enabled": True,
        "incident_response_plan": True,
        "log_monitoring_enabled": True
    }
}

# Simulated system settings (normally pulled from configurations)
system_settings = {
    "password_expiration_days": 120,  # Non-compliant (PCI DSS requires 90 days)
    "multi_factor_required": True,
    "logs_retention_days": 180,  # Non-compliant (PCI DSS requires 365)
    "data_encryption": True,
    "user_consent_required": True,
    "right_to_erasure_enabled": False,  # Non-compliant (GDPR requires this)
    "access_control_enabled": True,
    "incident_response_plan": False,  # Non-compliant (SOC 2 requires this)
    "log_monitoring_enabled": True
}

# Check compliance violations
violations = []
for standard, requirements in security_policies.items():
    for policy, expected_value in requirements.items():
        actual_value = system_settings.get(policy)
        if actual_value != expected_value:
            violations.append({
                "standard": standard,
                "policy": policy,
                "expected": expected_value,
                "actual": actual_value
            })

# Save compliance violations
with open("compliance_violations.json", "w") as f:
    json.dump(violations, f, indent=4)

print(f"✅ AI Found {len(violations)} Compliance Violations!")

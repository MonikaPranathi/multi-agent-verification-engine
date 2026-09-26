from agents.self_correction import self_correct


supply_chain = {
    "disruption": "major flood",
    "affected_location": "Chennai",
    "affected_supplier": "unknown",
    "affected_component": "electronic components",
    "downstream_dependencies": ["Andhra Electronics"]
}

risk = {
    "risk_score": 80,
    "risk_level": "HIGH"
}

action_plan = {
    "recommendation":
        "Formulate a contingency sourcing strategy."
}

evidence_verification = {
    "passed": False,
    "evidence_status": "INSUFFICIENT",
    "unsupported_claims": [
        "Alternative suppliers are available and qualified."
    ],
    "missing_evidence": [
        "Official flood impact report",
        "Current inventory",
        "Verified alternative suppliers",
        "Lead-time and pricing information"
    ],
    "contradictions": []
}


result = self_correct(
    supply_chain,
    risk,
    action_plan,
    evidence_verification
)

print("\n========== SELF CORRECTION ==========\n")
print(result)


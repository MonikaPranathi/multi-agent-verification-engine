from verification.evidence_verifier import verify_evidence


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

corrected_plan = {
    "correction_status":
        "Updated to reflect evidence gaps and prioritize information gathering",

    "revised_priority": "HIGH",

    "revised_immediate_actions": [
        "Request an official flood impact report",
        "Request current inventory levels",
        "Compile previously vetted alternative suppliers"
    ],

    "revised_recommendation":
        "Do not commit to new contracts or volume shifts "
        "until supporting evidence is obtained.",

    "evidence_to_collect": [
        "Official flood impact report",
        "Current inventory quantities",
        "Verified alternative suppliers",
        "Lead-time and pricing information"
    ],

    "remaining_uncertainties": [
        "Identity of affected supplier",
        "Flood severity and duration",
        "Availability of qualified alternative suppliers"
    ]
}


verification = verify_evidence(
    supply_chain,
    risk,
    corrected_plan
)

print("\n========== RE-VERIFICATION ==========\n")
print(verification)

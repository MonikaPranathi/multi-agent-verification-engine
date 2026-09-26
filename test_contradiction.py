from verification.contradiction_hunter import detect_contradictions


claims = [
    {
        "source": "Supplier status report",
        "claim": "The Chennai component supplier is operating normally."
    },
    {
        "source": "Local disruption report",
        "claim": "The Chennai component supplier has suspended operations because of flooding."
    },
    {
        "source": "Logistics report",
        "claim": "Road transportation from the supplier location is currently disrupted."
    }
]


result = detect_contradictions(claims)

print("\n========== CONTRADICTION HUNTER ==========\n")
print(result)

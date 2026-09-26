def get_demo_evidence():
    evidence = [
        {
            "source": "Supplier Status Report",
            "claim": "The Chennai component supplier is operating normally.",
            "confidence": 0.80
        },
        {
            "source": "Local Disruption Report",
            "claim": "The Chennai component supplier has suspended operations because of flooding.",
            "confidence": 0.90
        },
        {
            "source": "Logistics Report",
            "claim": "Road transportation from the supplier location is currently disrupted.",
            "confidence": 0.85
        }
    ]

    return evidence

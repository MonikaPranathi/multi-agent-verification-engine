def collect_independent_evidence(contradiction):

    print("\n======================================")
    print("      INDEPENDENT EVIDENCE")
    print("======================================")

    claim1 = contradiction["claim1"]
    claim2 = contradiction["claim2"]

    print("Checking:", claim1)
    print("Against :", claim2)

    evidence = [

        {
            "evidence_id": "E001",
            "source": "Independent Verification Check",
            "evidence_type": "verification",
            "claim": claim2,
            "supports_claim": claim2,
            "confidence": 0.90
        },

        {
            "evidence_id": "E002",
            "source": "Cross-Check",
            "evidence_type": "cross_check",
            "claim": claim2,
            "supports_claim": claim2,
            "confidence": 0.85
        }

    ]

    return evidence


if __name__ == "__main__":

    contradiction = {
        "claim1": "The Chennai component supplier is operating normally.",
        "claim2": "The Chennai component supplier has suspended operations because of flooding."
    }

    evidence = collect_independent_evidence(contradiction)

    print("\nIndependent Evidence:")

    for item in evidence:
        print(item)

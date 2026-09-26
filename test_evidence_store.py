from verification.evidence_store import get_demo_evidence


evidence = get_demo_evidence()

print("\n========== EVIDENCE STORE ==========\n")

for item in evidence:
    print("Source:", item["source"])
    print("Claim:", item["claim"])
    print("Confidence:", item["confidence"])
    print()

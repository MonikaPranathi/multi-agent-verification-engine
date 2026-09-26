def decide_next_step(
    calculation_verification: dict,
    evidence_verification: dict,
    contradiction_result: dict
) -> dict:

    # 1. Calculation verification failed
    if not calculation_verification.get("passed", False):

        return {
            "decision": "REJECT",
            "next_action": "recalculate_risk",
            "reason": "Risk calculation verification failed."
        }

    # 2. High-severity contradiction detected
    contradiction_data = contradiction_result.get("result", {})

    if (
        contradiction_data.get("contradiction_detected", False)
        and contradiction_data.get("severity") == "HIGH"
    ):

        return {
            "decision": "REPLAN",
            "next_action": "resolve_contradiction",
            "reason": (
                "High-severity contradiction detected. "
                "Independent evidence is required before "
                "accepting the recommendation."
            )
        }

    # 3. Evidence is insufficient
    if not evidence_verification.get("passed", False):

        return {
            "decision": "REPLAN",
            "next_action": "request_more_evidence",
            "reason": (
                "Evidence verification failed. "
                "More evidence is required before accepting "
                "the recommendation."
            )
        }

    # 4. Everything passed
    return {
        "decision": "ACCEPT",
        "next_action": "finalize",
        "reason": "All verification checks passed."
    }

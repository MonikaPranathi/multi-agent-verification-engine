from tools.risk_engine import calculate_risk


def verify_risk(supply_chain: dict, reported_risk: dict) -> dict:

    # Independently recalculate the risk
    verified_risk = calculate_risk(supply_chain)

    reported_score = reported_risk.get("risk_score")
    verified_score = verified_risk.get("risk_score")

    reported_level = reported_risk.get("risk_level")
    verified_level = verified_risk.get("risk_level")

    score_match = reported_score == verified_score
    level_match = reported_level == verified_level

    passed = score_match and level_match

    return {
        "verification_type": "calculation",
        "passed": passed,
        "reported_score": reported_score,
        "verified_score": verified_score,
        "reported_level": reported_level,
        "verified_level": verified_level,
        "score_match": score_match,
        "level_match": level_match,
        "message": (
            "Risk calculation verified successfully."
            if passed
            else "Risk calculation mismatch detected."
        )
    }


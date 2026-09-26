def calculate_risk(supply_chain: dict) -> dict:

    score = 0
    reasons = []

    disruption = supply_chain.get("disruption", "").lower()
    component = supply_chain.get("affected_component", "").lower()
    downstream = supply_chain.get("downstream_dependencies", [])

    # Disruption severity
    if "flood" in disruption:
        score += 30
        reasons.append("Flood disruption detected")

    elif "earthquake" in disruption:
        score += 40
        reasons.append("Earthquake disruption detected")

    elif "fire" in disruption:
        score += 35
        reasons.append("Fire disruption detected")

    else:
        score += 10
        reasons.append("Unknown disruption type")

    # Component dependency
    if component != "unknown" and component:
        score += 20
        reasons.append("Component supply is affected")

    # Downstream dependency
    if len(downstream) > 0:
        score += 20
        reasons.append("Downstream business dependency exists")

    # Missing supplier information
    if supply_chain.get("affected_supplier") == "unknown":
        score += 10
        reasons.append("Supplier identity is unknown")

    # Cap score
    score = min(score, 100)

    # Risk category
    if score >= 70:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }

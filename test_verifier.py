from agents.supply_chain_mapper import supply_chain_mapper
from tools.risk_engine import calculate_risk
from verification.calculation_verifier import verify_risk


input_text = """
A major flood has disrupted a component supplier in Chennai.
The supplier provides electronic components to Andhra Electronics.
"""

# 1. Mapper
mapped = supply_chain_mapper(input_text)

print("\n========== MAPPER ==========\n")
print(mapped)

if mapped["success"]:

    # 2. Risk calculation
    risk = calculate_risk(mapped["data"])

    print("\n========== RISK ==========\n")
    print(risk)

    # 3. Independent verification
    wrong_risk = {
        "risk_score": 90,
        "risk_level": "HIGH"
    }

    verification = verify_risk(
    mapped["data"],
    wrong_risk
    )

    print("\n========== VERIFICATION ==========\n")
    print(verification)


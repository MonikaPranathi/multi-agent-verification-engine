from agents.supply_chain_mapper import supply_chain_mapper
from tools.risk_engine import calculate_risk


input_text = """
A major flood has disrupted a component supplier in Chennai.
The supplier provides electronic components to Andhra Electronics.
"""

mapped = supply_chain_mapper(input_text)

print("\n========== MAPPER OUTPUT ==========\n")
print(mapped)

if mapped["success"]:

    risk = calculate_risk(mapped["data"])

    print("\n========== RISK ANALYSIS ==========\n")
    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])

    print("\nReasons:")

    for reason in risk["reasons"]:
        print("-", reason)

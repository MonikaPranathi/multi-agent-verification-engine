from agents.supply_chain_mapper import supply_chain_mapper
from tools.risk_engine import calculate_risk
from agents.action_planner import create_action_plan


input_text = """
A major flood has disrupted a component supplier in Chennai.
The supplier provides electronic components to Andhra Electronics.
"""

# 1. Map the supply chain
mapped = supply_chain_mapper(input_text)

print("\n========== MAPPER ==========\n")
print(mapped)

# 2. Calculate risk
if mapped["success"]:

    risk = calculate_risk(mapped["data"])

    print("\n========== RISK ==========\n")
    print(risk)

    # 3. Create action plan
    plan = create_action_plan(
        mapped["data"],
        risk
    )

    print("\n========== ACTION PLAN ==========\n")
    print(plan)

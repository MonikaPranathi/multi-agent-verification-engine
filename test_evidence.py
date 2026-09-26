from agents.supply_chain_mapper import supply_chain_mapper
from tools.risk_engine import calculate_risk
from agents.action_planner import create_action_plan
from verification.evidence_verifier import verify_evidence


input_text = """
A major flood has disrupted a component supplier in Chennai.
The supplier provides electronic components to Andhra Electronics.
"""

# 1. Mapper
mapped = supply_chain_mapper(input_text)

print("\n========== MAPPER ==========\n")
print(mapped)

if mapped["success"]:

    # 2. Risk Engine
    risk = calculate_risk(mapped["data"])

    print("\n========== RISK ==========\n")
    print(risk)

    # 3. Action Planner
    plan = create_action_plan(
        mapped["data"],
        risk
    )

    print("\n========== ACTION PLAN ==========\n")
    print(plan)

    if plan["success"]:

        # 4. Evidence Verification
        verification = verify_evidence(
            mapped["data"],
            risk,
            plan["plan"]
        )

        print("\n========== EVIDENCE VERIFICATION ==========\n")
        print(verification)


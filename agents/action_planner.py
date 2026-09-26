from llm.router import generate_response
import json


def create_action_plan(supply_chain: dict, risk: dict) -> dict:

    prompt = f"""
You are an Action Planning Agent for a supply chain
disruption response system.

Supply chain information:
{supply_chain}

Risk analysis:
{risk}

Create a practical response plan for the company.

Return ONLY valid JSON:

{{
    "priority": "",
    "immediate_actions": [],
    "short_term_actions": [],
    "recommendation": "",
    "required_evidence": [],
    "uncertainties": []
}}

Rules:
- Do not invent suppliers, prices, dates, or external facts.
- Base the plan only on the supplied information.
- If information is missing, identify it under uncertainties.
- Every recommendation should mention what evidence would be
  needed before the company acts on it.
- Return JSON only.
"""

    result = generate_response(prompt)

    # LLM failed → use deterministic fallback plan
    if not result["success"]:
        print("LLM providers unavailable. Using fallback action plan.")

        fallback_plan = {
            "priority": risk.get("risk_level", "MEDIUM"),

            "immediate_actions": [
                "Confirm the disruption and affected supplier details",
                "Assess current production and transportation impact",
                "Check available inventory and alternative supply options"
            ],

            "short_term_actions": [
                "Identify alternative suppliers if required",
                "Monitor transportation and production status",
                "Collect supporting evidence before making major decisions"
            ],

            "recommendation": (
                "Temporarily assess the disruption using the available "
                "information and collect additional evidence before "
                "taking major action."
            ),

            "required_evidence": [
                "Supplier disruption confirmation",
                "Transportation status",
                "Production impact information"
            ],

            "uncertainties": [
                "Supplier identity is unknown",
                "Affected component is unknown",
                "Downstream impact is not confirmed"
            ]
        }

        return {
            "success": True,
            "provider": "fallback",
            "plan": fallback_plan
        }

    response = result["response"]

    response = response.replace("```json", "").replace("```", "").strip()

    try:
        plan = json.loads(response)

        return {
            "success": True,
            "provider": result["provider"],
            "plan": plan
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "provider": result["provider"],
            "error": "Model returned invalid JSON",
            "raw_response": response
        }

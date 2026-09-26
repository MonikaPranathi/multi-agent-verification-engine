from llm.router import generate_response
import json


def self_correct(
    supply_chain: dict,
    risk: dict,
    action_plan: dict,
    evidence_verification: dict
) -> dict:

    prompt = f"""
You are a Self-Correction Agent in a supply chain
decision verification system.

Your job is to improve an AI-generated action plan after
an independent verifier found insufficient evidence.

SUPPLY CHAIN:
{supply_chain}

RISK:
{risk}

ORIGINAL ACTION PLAN:
{action_plan}

EVIDENCE VERIFICATION:
{evidence_verification}

Create a revised action plan.

Requirements:
- Do NOT pretend missing evidence exists.
- Do NOT invent suppliers, prices, dates, inventory,
  flood reports, or other facts.
- Remove or weaken unsupported claims.
- Clearly identify what must be verified before taking
  high-impact actions.
- Prefer information-gathering and low-risk actions
  when evidence is insufficient.
- The revised plan must explicitly address the missing
  evidence identified by the verifier.

Return ONLY valid JSON:

{{
    "correction_status": "",
    "revised_priority": "",
    "revised_immediate_actions": [],
    "revised_short_term_actions": [],
    "revised_recommendation": "",
    "evidence_to_collect": [],
    "remaining_uncertainties": []
}}

Rules:
- Return JSON only.
- Do not add markdown.
"""

    result = generate_response(prompt)

    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }

    response = result["response"]

    response = response.replace("```json", "").replace("```", "").strip()

    try:
        corrected_plan = json.loads(response)

        return {
            "success": True,
            "provider": result["provider"],
            "corrected_plan": corrected_plan
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "provider": result["provider"],
            "error": "Model returned invalid JSON",
            "raw_response": response
        }

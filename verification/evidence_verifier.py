from llm.router import generate_response
import json


def verify_evidence(supply_chain: dict, risk: dict, action_plan: dict) -> dict:

    prompt = f"""
You are an independent Evidence Verification Agent.

Your job is to verify whether an AI-generated supply chain
recommendation is sufficiently supported by the available information.

SUPPLY CHAIN INFORMATION:
{supply_chain}

RISK ANALYSIS:
{risk}

ACTION PLAN:
{action_plan}

Analyze the recommendation carefully.

Check:
1. What claims are being made?
2. Is each important claim supported by the provided information?
3. What evidence is missing?
4. Are there unsupported assumptions?
5. Are there contradictions?
6. Should the recommendation be accepted or rejected?

Return ONLY valid JSON in this exact structure:

{{
    "passed": false,
    "evidence_status": "INSUFFICIENT",
    "unsupported_claims": [],
    "missing_evidence": [],
    "contradictions": [],
    "reason": ""
}}

Rules:
- Do not invent evidence.
- Do not assume missing information is true.
- If evidence is insufficient, set passed to false.
- Keep missing information separate from confirmed facts.
- Be conservative when verifying important business decisions.
- Return JSON only.
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
        verification = json.loads(response)

        return {
            "success": True,
            "provider": result["provider"],
            "verification": verification
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "provider": result["provider"],
            "error": "Model returned invalid JSON",
            "raw_response": response
        }

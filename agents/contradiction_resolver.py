from llm.router import generate_response
import json


def resolve_contradiction(claim1, claim2, evidence):

    prompt = f"""
You are a Contradiction Resolution Agent.

Two claims conflict:

CLAIM 1:
{claim1}

CLAIM 2:
{claim2}

Independent evidence:
{evidence}

Determine which claim is better supported by the independent evidence.

Return ONLY valid JSON:

{{
    "resolved": true,
    "status": "RESOLVED",
    "accepted_claim": "",
    "rejected_claim": "",
    "reason": "",
    "required_evidence": []
}}

Rules:
- Accept a claim only if the evidence supports it.
- Do not invent facts.
- If evidence is insufficient, set resolved to false.
- If both claims remain possible, set status to "UNRESOLVED".
- Return JSON only.
"""

    result = generate_response(prompt)

    # LLM failed → deterministic evidence-based fallback
    if not result["success"]:

        print("LLM providers unavailable. Using fallback contradiction resolution.")

        claim1_support = 0.0
        claim2_support = 0.0

        for item in evidence:

            supported = item.get("supports_claim", "")
            confidence = item.get("confidence", 0)

            if supported == claim1:
                claim1_support += confidence

            if supported == claim2:
                claim2_support += confidence

        if claim1_support > claim2_support:

            return {
                "resolved": True,
                "status": "RESOLVED",
                "accepted_claim": claim1,
                "rejected_claim": claim2,
                "reason": (
                    "Independent evidence provides stronger support "
                    "for Claim 1."
                ),
                "required_evidence": []
            }

        elif claim2_support > claim1_support:

            return {
                "resolved": True,
                "status": "RESOLVED",
                "accepted_claim": claim2,
                "rejected_claim": claim1,
                "reason": (
                    "Independent evidence provides stronger support "
                    "for Claim 2."
                ),
                "required_evidence": []
            }

        else:

            return {
                "resolved": False,
                "status": "UNRESOLVED",
                "accepted_claim": None,
                "rejected_claim": None,
                "reason": (
                    "Independent evidence is insufficient "
                    "to determine which claim is correct."
                ),
                "required_evidence": [
                    "Additional independent evidence is required."
                ]
            }

    response = result["response"]

    response = response.replace("```json", "").replace("```", "").strip()

    try:

        resolution = json.loads(response)

        return resolution

    except json.JSONDecodeError:

        return {
            "resolved": False,
            "status": "UNRESOLVED",
            "accepted_claim": None,
            "rejected_claim": None,
            "reason": "Model returned invalid JSON.",
            "required_evidence": [
                "Valid contradiction resolution response"
            ]
        }

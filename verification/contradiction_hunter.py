from llm.router import generate_response
import json


def detect_contradictions(claims: list) -> dict:

    prompt = f"""
You are an independent Contradiction Detection Agent.

Analyze the following claims/evidence:

{claims}

Determine whether any claims directly or materially
contradict each other.

Return ONLY valid JSON:

{{
    "contradiction_detected": false,
    "contradictions": [],
    "affected_claims": [],
    "severity": "NONE",
    "reason": ""
}}

Rules:
- Do not invent contradictions.
- Only identify contradictions supported by the provided claims.
- If claims are merely incomplete, do not call them contradictory.
- If two claims cannot both reasonably be true at the same time,
  identify the contradiction.
- Use severity: NONE, LOW, MEDIUM, or HIGH.
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
        contradiction_result = json.loads(response)

        return {
            "success": True,
            "provider": result["provider"],
            "result": contradiction_result
        }


    except json.JSONDecodeError:
        return {
            "success": False,
            "provider": result["provider"],
            "error": "Model returned invalid JSON",
            "raw_response": response
        }

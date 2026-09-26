from llm.router import generate_response
import json


def supply_chain_mapper(disruption: str) -> dict:

    prompt = f"""
You are a Supply Chain Mapping Agent.

Your job is to analyze a supply chain disruption and extract the
affected entities and dependencies.

Disruption:
{disruption}

Return ONLY valid JSON in this exact structure:

{{
    "disruption": "",
    "affected_location": "",
    "affected_supplier": "",
    "affected_component": "",
    "upstream_dependencies": [],
    "downstream_dependencies": [],
    "impact_area": "",
    "assumptions": []
}}

Rules:
- Do not invent specific facts.
- If information is missing, write "unknown".
- Keep assumptions separate from known information.
- Return JSON only.
"""

    result = generate_response(prompt)

    # LLM failed → deterministic fallback
    if not result["success"]:

        print("LLM providers unavailable. Using fallback supply-chain mapping.")

        text = disruption.lower()

        # Location detection
        if "chennai" in text:
            location = "Chennai"
        else:
            location = "unknown"

        # Disruption type
        if "flood" in text or "flooding" in text:
            disruption_type = "flood"
        elif "earthquake" in text:
            disruption_type = "earthquake"
        elif "fire" in text:
            disruption_type = "fire"
        else:
            disruption_type = "unknown"

        # Impact area
        impact_area = "unknown"

        if "production" in text and "transportation" in text:
            impact_area = "production and transportation"
        elif "production" in text:
            impact_area = "production"
        elif "transportation" in text:
            impact_area = "transportation"

        assumptions = [
            "The specific name of the component supplier is not provided.",
            "The type of component supplied is not specified.",
            "No explicit upstream or downstream entities are identified."
        ]

        return {
            "success": True,
            "provider": "fallback",
            "data": {
                "disruption": disruption,
                "affected_location": location,
                "affected_supplier": "unknown",
                "affected_component": "unknown",
                "upstream_dependencies": [],
                "downstream_dependencies": [],
                "impact_area": impact_area,
                "assumptions": assumptions
            }
        }

    response = result["response"]

    # Remove markdown code fences
    response = response.replace("```json", "").replace("```", "").strip()

    try:

        mapped_data = json.loads(response)

        return {
            "success": True,
            "provider": result["provider"],
            "data": mapped_data
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "provider": result["provider"],
            "error": "Model returned invalid JSON",
            "raw_response": response
        }

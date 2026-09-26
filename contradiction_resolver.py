from groq import Groq
import os
import json


def resolve_contradiction(contradiction, independent_evidence):

    print("\n======================================")
    print("      CONTRADICTION RESOLUTION")
    print("======================================")

    claim1 = contradiction.get("claim1", "")
    claim2 = contradiction.get("claim2", "")

    print("Claim 1:", claim1)
    print("Claim 2:", claim2)

    print("\nIndependent Evidence:")

    for evidence in independent_evidence:
        print(evidence)

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""
You are a contradiction resolution agent.

Two claims are in conflict.

CLAIM 1:
{claim1}

CLAIM 2:
{claim2}

INDEPENDENT EVIDENCE:
{json.dumps(independent_evidence, indent=2)}

Your task is to determine whether the contradiction can be resolved using
the independent evidence.

Rules:

1. Compare CLAIM 1 and CLAIM 2 carefully.
2. Examine every independent evidence item.
3. Do not assume that evidence is true merely because it has high confidence.
4. If the evidence clearly supports one claim and contradicts the other,
   resolve the contradiction.
5. If the evidence is insufficient or does not clearly support either claim,
   mark the contradiction as UNRESOLVED.
6. Never invent missing information.

Return ONLY valid JSON in this exact format:

{{
    "resolved": true or false,
    "status": "RESOLVED" or "UNRESOLVED",
    "reason": "Explain why the contradiction was or was not resolved.",
    "accepted_claim": "The supported claim, or null if unresolved.",
    "required_evidence": []
}}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content

        return json.loads(result)

    except Exception as e:

        return {
            "resolved": False,
            "status": "ERROR",
            "reason": str(e),
            "accepted_claim": None,
            "required_evidence": [
                "Valid contradiction resolution could not be obtained."
            ]
        }

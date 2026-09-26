from llm.router import generate_response


result = generate_response(
    "What is supply chain disruption? Explain in one sentence."
)

print("\nProvider:", result["provider"])
print("Success:", result["success"])
print("Response:", result["response"])

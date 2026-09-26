from llm.groq_client import ask_groq

response = ask_groq(
    "Explain multi-agent AI in one simple sentence."
)

print(response)

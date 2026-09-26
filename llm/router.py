from llm.groq_client import ask_groq
from llm.gemini import ask_gemini


def generate_response(prompt: str) -> dict:

    # Primary provider: Groq
    try:
        response = ask_groq(prompt)

        return {
            "provider": "groq",
            "success": True,
            "response": response
        }

    except Exception as e:

        print(f"Groq failed: {e}")
        print("Switching to Gemini...")

    # Backup provider: Gemini
    try:
        response = ask_gemini(prompt)

        return {
            "provider": "gemini",
            "success": True,
            "response": response
        }

    except Exception as e:

        return {
            "provider": None,
            "success": False,
            "response": None,
            "error": str(e)
        }

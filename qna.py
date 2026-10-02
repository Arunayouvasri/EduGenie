from gemini_client import generate_text, GeminiQuotaError


def fallback_answer(question: str) -> str:
    question_lower = question.lower().strip()

    # Photosynthesis
    if "photosynthesis" in question_lower:
        return """Photosynthesis is the process by which green plants make their own food using sunlight.

Plants use:
- Sunlight
- Water
- Carbon dioxide

They produce:
- Glucose (food)
- Oxygen

In simple words, plants use sunlight as energy to convert water and carbon dioxide into food."""

    # Recursion
    if "recursion" in question_lower:
        return """Recursion is a programming technique where a function calls itself to solve a smaller version of the same problem.

A recursive function needs:
- Base case — tells the function when to stop.
- Recursive step — calls the function again with a smaller input.

Example: countdown(3) → 3 → 2 → 1 → 0."""

    # Python
    if "python" in question_lower:
        return """Python is a high-level, general-purpose programming language.

It is commonly used for:
- Web development
- Data analysis
- Artificial intelligence
- Automation
- Software development

Python is popular because its syntax is simple and easy to read."""

    # Largest Ocean
    if "largest ocean" in question_lower:
        return """The Pacific Ocean is the largest ocean on Earth.

It is located between Asia and Australia on the west and North and South America on the east."""

    # Generic fallback
    return f"""Here is a basic explanation of your question:

{question}

Gemini is currently unavailable because the daily API quota has been reached.
Please try again after the quota resets for a detailed AI-generated answer."""


def answer_question(question: str) -> str:

    prompt = f"""You are EduGenie, a student-friendly educational assistant.

Answer the question below accurately and concisely.

Use simple language, short paragraphs, and examples when useful.

Do not invent sources or facts. If the question is ambiguous, state the assumption.

Question:

{question}
"""

    try:
        return generate_text(
            prompt,
            temperature=0.3,
            max_output_tokens=1200
        )

    except GeminiQuotaError:
        return fallback_answer(question)

    except Exception as exc:
        return f"Unable to answer right now: {exc}"
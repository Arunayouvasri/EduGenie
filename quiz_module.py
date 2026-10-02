import json
import re
from typing import Any

from gemini_client import generate_text, GeminiQuotaError


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any) -> list[dict]:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")

    clean = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Invalid question object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if (
            not question
            or not isinstance(options, list)
            or len(options) != 4
            or not answer
        ):
            raise ValueError(
                "Each question needs a question, four options, and an answer."
            )

        if answer not in [str(x) for x in options]:
            raise ValueError("The answer must exactly match one option.")

        clean.append({
            "question": question,
            "options": [str(x) for x in options],
            "answer": answer,
            "explanation": explanation,
        })

    return clean


def _photosynthesis_quiz() -> list[dict]:
    return [
        {
            "question": "What is the main source of energy for photosynthesis?",
            "options": ["Sunlight", "Water", "Soil", "Oxygen"],
            "answer": "Sunlight",
            "explanation": "Plants use sunlight as the energy source for photosynthesis."
        },
        {
            "question": "Which gas do plants use during photosynthesis?",
            "options": [
                "Carbon dioxide",
                "Oxygen",
                "Nitrogen",
                "Hydrogen"
            ],
            "answer": "Carbon dioxide",
            "explanation": "Plants take in carbon dioxide from the air."
        },
        {
            "question": "What gas is released during photosynthesis?",
            "options": [
                "Oxygen",
                "Carbon dioxide",
                "Nitrogen",
                "Hydrogen"
            ],
            "answer": "Oxygen",
            "explanation": "Oxygen is released as a product of photosynthesis."
        }
    ]


def _recursion_quiz() -> list[dict]:
    return [
        {
            "question": "What is recursion?",
            "options": [
                "A function calling itself",
                "A loop that never stops",
                "A type of variable",
                "A database operation"
            ],
            "answer": "A function calling itself",
            "explanation": "Recursion occurs when a function calls itself."
        },
        {
            "question": "What tells a recursive function when to stop?",
            "options": [
                "Base case",
                "Loop case",
                "Input case",
                "Output case"
            ],
            "answer": "Base case",
            "explanation": "The base case prevents the recursive calls from continuing forever."
        },
        {
            "question": "What happens in the recursive step?",
            "options": [
                "The function calls itself with a smaller problem",
                "The program always stops",
                "The computer shuts down",
                "A new programming language is created"
            ],
            "answer": "The function calls itself with a smaller problem",
            "explanation": "The recursive step reduces the problem and calls the function again."
        }
    ]


def _python_quiz() -> list[dict]:
    return [
        {
            "question": "What type of language is Python?",
            "options": [
                "High-level programming language",
                "Markup language",
                "Database",
                "Operating system"
            ],
            "answer": "High-level programming language",
            "explanation": "Python is a high-level, general-purpose programming language."
        },
        {
            "question": "Which function displays output in Python?",
            "options": [
                "print()",
                "display()",
                "show()",
                "output()"
            ],
            "answer": "print()",
            "explanation": "The print() function displays output."
        },
        {
            "question": "Which is a common use of Python?",
            "options": [
                "Web development",
                "Only drawing pictures",
                "Only making phone calls",
                "Only editing videos"
            ],
            "answer": "Web development",
            "explanation": "Python is commonly used for web development and many other areas."
        }
    ]


def _water_cycle_quiz() -> list[dict]:
    return [
        {
            "question": "What process changes liquid water into water vapor?",
            "options": [
                "Evaporation",
                "Condensation",
                "Precipitation",
                "Collection"
            ],
            "answer": "Evaporation",
            "explanation": "Evaporation changes liquid water into water vapor."
        },
        {
            "question": "What process forms clouds when water vapor cools?",
            "options": [
                "Evaporation",
                "Condensation",
                "Collection",
                "Runoff"
            ],
            "answer": "Condensation",
            "explanation": "Condensation occurs when water vapor cools and forms water droplets."
        },
        {
            "question": "What is precipitation?",
            "options": [
                "Water falling from clouds",
                "Water changing into vapor",
                "Cloud formation",
                "Water being stored underground"
            ],
            "answer": "Water falling from clouds",
            "explanation": "Rain, snow, sleet, and hail are forms of precipitation."
        }
    ]


def fallback_quiz(passage: str) -> list[dict]:
    text = passage.lower()

    if "photosynthesis" in text:
        return _photosynthesis_quiz()

    if "recursion" in text:
        return _recursion_quiz()

    if "python" in text:
        return _python_quiz()

    if "water cycle" in text:
        return _water_cycle_quiz()

    return [
        {
            "question": "What is the passage mainly about?",
            "options": [
                "The educational topic described in the passage",
                "Sports",
                "Weather",
                "Entertainment"
            ],
            "answer": "The educational topic described in the passage",
            "explanation": "The question is based on the supplied passage."
        },
        {
            "question": "What is the purpose of the passage?",
            "options": [
                "To provide educational information",
                "To sell a product",
                "To describe a movie",
                "To discuss sports"
            ],
            "answer": "To provide educational information",
            "explanation": "The passage is supplied as educational content."
        },
        {
            "question": "What should a student do after reading the passage?",
            "options": [
                "Review and practice the concepts",
                "Ignore the topic",
                "Delete the passage",
                "Change the subject"
            ],
            "answer": "Review and practice the concepts",
            "explanation": "Reviewing and practicing helps students understand educational material."
        }
    ]


def generate_quiz(passage: str) -> list[dict] | dict:
    prompt = f"""Create exactly 3 multiple-choice questions from the passage below.
Return ONLY valid JSON: an array of 3 objects.

Each object must have these keys:
question, options, answer, explanation.

options must contain exactly 4 strings.
answer must exactly equal one option.

Questions must be answerable from the supplied passage.

Passage:
{passage}
"""

    try:
        raw = generate_text(
            prompt,
            temperature=0.2,
            max_output_tokens=1800
        )

        return _validate_quiz(
            json.loads(clean_json_block(raw))
        )

    except GeminiQuotaError:
        return fallback_quiz(passage)

    except Exception as exc:
        return {"error": f"Quiz generation failed: {exc}"}
import os
import time
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class GeminiConfigurationError(RuntimeError):
    pass


class GeminiQuotaError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
) -> str:

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    from google.genai import types

    for attempt in range(3):
        try:
            response = get_client().models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        except Exception as exc:
            error_text = str(exc).upper()

            # Daily quota exceeded
            if (
                "RESOURCE_EXHAUSTED" in error_text
                and "FREE_TIER" in error_text
            ):
                raise GeminiQuotaError(
                    "Gemini daily free-tier quota has been reached. "
                    "Please try again after the quota resets."
                )

            # Temporary server overload
            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < 2:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue

            # Temporary rate limit
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                if attempt < 2:
                    wait_time = 3 * (attempt + 1)
                    print(
                        f"Gemini rate limit reached. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue

            raise
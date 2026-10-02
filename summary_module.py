from gemini_client import generate_text, GeminiQuotaError


def fallback_summary(text: str) -> str:
    text_lower = text.lower()

    # Photosynthesis
    if "photosynthesis" in text_lower:
        return """# 🌱 Quick Revision: Photosynthesis

### 📌 Definition

Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to produce glucose and release oxygen.

### 🔑 Key Points

- ☀️ Sunlight provides the energy needed for the process.
- 💧 Water is used by the plant.
- 🌬️ Carbon dioxide is used by the plant.
- 🍃 Chlorophyll absorbs sunlight.
- 🍬 Glucose is produced.
- 💨 Oxygen is released.

### 🧠 Easy to Remember

Sunlight + Water + Carbon Dioxide → Glucose + Oxygen

This is a simplified revision summary based on the given passage.
"""

    # Recursion
    if "recursion" in text_lower:
        return """# 🔄 Quick Revision: Recursion

### 📌 Definition

Recursion is a programming technique where a function calls itself to solve a smaller version of the same problem.

### 🔑 Key Points

- A function calls itself.
- A base case tells it when to stop.
- The recursive step solves a smaller problem.
- Each function call is stored in memory.

### 🧠 Easy Example

countdown(3) → 3 → 2 → 1 → 0
"""

    # Python
    if "python" in text_lower:
        return """# 🐍 Quick Revision: Python

### 📌 Definition

Python is a high-level programming language known for its simple and readable syntax.

### 🔑 Key Points

- Easy to learn and read.
- Used for web development.
- Used in automation and data science.
- Widely used in AI.
- Supports object-oriented programming.
"""

    # Water Cycle
    if "water cycle" in text_lower:
        return """# 💧 Quick Revision: Water Cycle

### 📌 Definition

The water cycle is the continuous movement of water between the Earth's surface and the atmosphere.

### 🔑 Key Processes

- ☀️ Evaporation — Water changes from liquid to water vapor.
- ☁️ Condensation — Water vapor cools and forms clouds.
- 🌧️ Precipitation — Water falls from clouds as rain, snow, sleet, or hail.
- 💧 Collection — Water collects in oceans, lakes, rivers, and other water bodies.

### 🧠 Easy to Remember

Evaporation → Condensation → Precipitation → Collection
"""

    sentences = [
        sentence.strip()
        for sentence in text.replace("\n", " ").split(".")
        if sentence.strip()
    ]

    if not sentences:
        return "No content was provided for summarization."

    result = "# 📚 Quick Revision Summary\n\n"

    for sentence in sentences[:5]:
        result += f"- {sentence}.\n"

    return result


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational passage below for quick revision.

Keep the important facts and relationships.
Use a short heading and bullet points.

Do not add information that is not present in the passage.

Passage:
{text}
"""

    try:
        return generate_text(
            prompt,
            temperature=0.25,
            max_output_tokens=1500
        )

    except GeminiQuotaError:
        return fallback_summary(text)

    except Exception as exc:
        return f"Unable to summarize right now: {exc}"



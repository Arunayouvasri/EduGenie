from gemini_client import generate_text, GeminiQuotaError


def _gemini_explanation(topic: str) -> str:
    prompt = f"""Explain the following topic to a beginner.

Give a proper educational explanation.

Start with a clear definition.
Then explain the main concepts in simple language.
Give important points and one simple example.

Topic:
{topic}
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1400
    )


def _fallback_explanation(topic: str) -> str:
    topic_lower = topic.lower().strip()

    # Object-Oriented Programming
    if (
        "object-oriented programming" in topic_lower
        or "object oriented programming" in topic_lower
        or "oops" in topic_lower
        or topic_lower == "oop"
    ):
        return """# 💻 Object-Oriented Programming

### 📌 Definition

Object-Oriented Programming (OOP) is a programming approach that organizes a program using objects and classes.

### 🔑 Main Concepts

- Class - A class is a blueprint or template used to create objects.
- Object - An object is an instance of a class.
- Encapsulation - It combines data and methods inside a single class.
- Inheritance - It allows one class to acquire properties and methods from another class.
- Polymorphism - It allows the same method or operation to behave differently in different situations.
- Abstraction - It hides unnecessary implementation details and shows only the important features.

### 🧠 Simple Example

Consider a class called Student.

A Student class can contain:

- Name
- Roll number
- Marks

It can also contain methods such as:

- displayDetails()
- calculateGrade()

When we create a student from this class, that student becomes an object.

### 💡 Easy Way to Remember

Class → Blueprint

Object → Real instance

OOP helps organize programs into reusable and manageable components.

"""

    # Recursion
    if "recursion" in topic_lower:
        return """# 🔄 Recursion

### 📌 Definition

Recursion is a programming technique where a function calls itself to solve a smaller version of the same problem.

### 🔑 Key Points

- A recursive function calls itself.
- A base case tells the function when to stop.
- The recursive step solves a smaller problem.
- Each function call is stored in memory.

### 🧠 Example

A countdown can work like this:

countdown(3) → 3 → 2 → 1 → 0

When the value reaches 0, the recursion stops.

### 💡 Easy Way to Remember

Function calls itself → Smaller problem → Base case → Stop
"""

    # Photosynthesis
    if "photosynthesis" in topic_lower:
        return """# 🌱 Photosynthesis

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
"""

    # Python
    if "python" in topic_lower:
        return """# 🐍 Python

### 📌 Definition

Python is a high-level, general-purpose programming language known for its simple and readable syntax.

### 🔑 Key Points

- Python is easy to learn and read.
- It supports object-oriented programming.
- It is used for web development.
- It is used for automation and data analysis.
- It is widely used in artificial intelligence.

### 💻 Example

name = "Arun"
print("Hello", name)

This program stores a name in a variable and displays it.

### 💡 Easy to Remember

Python = Simple syntax + Many applications
"""

    # Generic fallback
    return f"""# 📚 {topic}

### 📌 Definition

{topic} is a topic that can be understood by learning its basic concepts, important terms, and practical examples.

### 🔑 How to Learn This Topic

- Start with the basic definition.
- Understand the important concepts.
- Study simple examples.
- Practice the concepts.
- Gradually move to advanced topics.

### 🧠 Example

Study the basic concepts of {topic} first and then practice them with simple examples.

Gemini is currently unavailable because the daily API quota has been reached. This is a fallback explanation.
"""


def explain_topic(topic: str) -> str:
    try:
        return _gemini_explanation(topic)

    except GeminiQuotaError:
        return _fallback_explanation(topic)

    except Exception as exc:
        return f"Unable to explain this topic right now: {exc}"
from gemini_client import generate_text, GeminiQuotaError


def fallback_learning_path(topic: str, level: str) -> str:
    topic_lower = topic.lower().strip()

    # Python
    if "python" in topic_lower:
        return f"""# 🐍 Python Learning Path

### Learner Level
{level.title()}

### 1. Fundamentals
- Python syntax
- Variables and data types
- Operators
- Input and output
- Conditional statements
- Loops

### 2. Core Concepts
- Strings
- Lists, tuples, sets, and dictionaries
- Functions
- Modules
- Exception handling

### 3. Object-Oriented Programming
- Classes and objects
- Constructors
- Inheritance
- Polymorphism
- Encapsulation

### 4. Advanced Topics
- File handling
- Iterators and generators
- Lambda functions
- Decorators
- Working with APIs

### 5. Practice Plan
- Week 1: Python basics
- Week 2: Functions and collections
- Week 3: OOP and file handling
- Week 4: Build a small Python project

### 6. Project Ideas
- Calculator
- Student Management System
- Quiz Application
- Library Management System
"""

    # Java
    if "java" in topic_lower:
        return f"""# ☕ Java Learning Path

### Learner Level
{level.title()}

### 1. Fundamentals
- Java syntax
- Variables and data types
- Operators
- Input and output
- Conditional statements
- Loops

### 2. Core Java
- Arrays
- Strings
- Methods
- Constructors
- Packages
- Exception handling

### 3. Object-Oriented Programming
- Classes and objects
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Interfaces

### 4. Advanced Topics
- Collections Framework
- ArrayList
- HashMap
- HashSet
- Generics
- File handling

### 5. Practice Plan
- Week 1: Java basics
- Week 2: Arrays, strings, and methods
- Week 3: OOP concepts
- Week 4: Collections and mini project

### 6. Project Ideas
- Student Management System
- Library Management System
- Banking Application
- Quiz Application
"""

    # SQL
    if "sql" in topic_lower or "database" in topic_lower or "dbms" in topic_lower:
        return f"""# 🗄️ SQL and Database Learning Path

### Learner Level
{level.title()}

### 1. Fundamentals
- Database basics
- Tables and records
- Primary keys
- Foreign keys
- SQL syntax

### 2. Basic SQL
- SELECT
- WHERE
- ORDER BY
- GROUP BY
- DISTINCT
- Aggregate functions

### 3. Intermediate SQL
- JOIN
- Subqueries
- Nested queries
- Views
- Constraints

### 4. Advanced Topics
- Normalization
- Transactions
- Indexing
- Stored procedures
- Database security

### 5. Practice Plan
- Week 1: SQL basics
- Week 2: Filtering and aggregation
- Week 3: Joins and subqueries
- Week 4: Build a database project

### 6. Project Ideas
- Student Database
- Library Database
- Employee Management Database
- Online Store Database
"""

    # HTML / CSS / JavaScript
    if "html" in topic_lower or "css" in topic_lower or "javascript" in topic_lower:
        return f"""# 🌐 Web Development Learning Path

### Learner Level
{level.title()}

### 1. HTML Fundamentals
- HTML structure
- Headings and paragraphs
- Links and images
- Forms
- Tables
- Semantic elements

### 2. CSS Fundamentals
- Selectors
- Colors and fonts
- Box model
- Flexbox
- Grid
- Responsive design

### 3. JavaScript
- Variables
- Data types
- Functions
- Conditions
- Loops
- Arrays and objects
- DOM manipulation

### 4. Advanced Topics
- Events
- Fetch API
- Async programming
- Form validation
- Local storage

### 5. Practice Plan
- Week 1: HTML
- Week 2: CSS
- Week 3: JavaScript
- Week 4: Build a responsive website

### 6. Project Ideas
- Portfolio Website
- To-Do List
- Calculator
- Quiz Website
"""

    # Object-Oriented Programming
    if (
        "object-oriented" in topic_lower
        or "object oriented" in topic_lower
        or "oops" in topic_lower
        or topic_lower == "oop"
    ):
        return f"""# 💻 Object-Oriented Programming Learning Path

### Learner Level
{level.title()}

### 1. Fundamentals
- What is OOP?
- Classes
- Objects
- Methods
- Constructors

### 2. Four Main Principles
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction

### 3. Intermediate Concepts
- Method overloading
- Method overriding
- Interfaces
- Access modifiers
- Static members

### 4. Advanced Concepts
- Abstract classes
- Multiple inheritance through interfaces
- Composition
- Association
- Design principles

### 5. Practice Plan
- Week 1: Classes and objects
- Week 2: Encapsulation and inheritance
- Week 3: Polymorphism and abstraction
- Week 4: Build an OOP-based project

### 6. Project Ideas
- Student Management System
- Bank Account System
- Library Management System
- Employee Management System
"""

    # Machine Learning
    if (
        "machine learning" in topic_lower
        or "machine-learning" in topic_lower
    ):
        return f"""# 🤖 Machine Learning Learning Path

### Learner Level
{level.title()}

### 1. Prerequisites
- Basic Python
- Basic mathematics
- Basic statistics
- Data handling

### 2. Fundamentals
- What is Machine Learning?
- Supervised learning
- Unsupervised learning
- Training and testing data
- Features and labels

### 3. Common Algorithms
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- K-Means Clustering

### 4. Model Evaluation
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

### 5. Practice Plan
- Week 1: Python and data basics
- Week 2: Machine learning fundamentals
- Week 3: Algorithms
- Week 4: Build a small ML project

### 6. Project Ideas
- Student Score Prediction
- House Price Prediction
- Spam Detection
- Simple Classification Project
"""

    # Generic topic-specific fallback
    words = topic.strip().split()
    topic_title = " ".join(word.capitalize() for word in words)

    return f"""# 📚 {topic_title} Learning Path

### Learner Level
{level.title()}

### 1. Introduction
- Understand what {topic} means.
- Learn why {topic} is used.
- Identify the basic terminology.

### 2. Fundamentals
- Learn the basic concepts of {topic}.
- Understand the important components.
- Study simple examples.
- Practice basic exercises.

### 3. Intermediate Concepts
- Learn the commonly used techniques in {topic}.
- Solve practical problems.
- Work with examples and exercises.
- Apply the concepts to small tasks.

### 4. Advanced Concepts
- Study advanced concepts related to {topic}.
- Explore real-world applications.
- Solve more complex problems.
- Build a small practical project.

### 5. 4-Week Practice Plan
- Week 1: Learn the fundamentals of {topic}.
- Week 2: Practice the core concepts.
- Week 3: Study intermediate and advanced concepts.
- Week 4: Build a small project using {topic}.

### 6. Project Ideas
- Create a basic project using {topic}.
- Solve practical problems related to {topic}.
- Build a small application to demonstrate what you learned.

### 7. Resources
- Official documentation
- Books
- Video tutorials
- Practice websites
"""


def get_learning_recommendations(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""Create a personalized learning path for the topic: {topic}

Learner level: {level}

The learning path must be specifically about {topic}.
Do NOT give a generic programming learning path.

Include:

1. Prerequisites
2. Beginner foundations
3. Intermediate topics
4. Advanced topics
5. A realistic 4-week timeline
6. Practice/project ideas
7. Useful resource types

Make every section relevant to {topic}.

Use simple language and clear headings.
Do not invent specific URLs.
"""

    try:
        return generate_text(
            prompt,
            temperature=0.45,
            max_output_tokens=2200
        )

    except GeminiQuotaError:
        return fallback_learning_path(topic, level)

    except Exception as exc:
        return f"Unable to create a learning path right now: {exc}"
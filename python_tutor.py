"""
Python Expert Tutor Module
Provides educational responses to Python questions with progressive learning
"""

from enum import Enum
from typing import Dict, List, Tuple

class SkillLevel(Enum):
    """Skill levels for users"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Python Learning Topics Database
PYTHON_TOPICS = {
    # BEGINNER TOPICS
    "variables": {
        "level": SkillLevel.BEGINNER,
        "keywords": ["variable", "var", "declare", "assign", "="],
        "explanation": {
            "beginner": "A variable is a named container that stores a value in memory. You create it by using a name and the = operator.",
            "intermediate": "Variables in Python are references to objects in memory. Python uses dynamic typing, so you don't declare types.",
            "advanced": "Variables are merely references to objects. Python stores the object in memory and the variable holds a pointer to it."
        },
        "code": """# Creating and using variables
name = "Alice"  # String variable
age = 25        # Integer variable
height = 5.6    # Float variable
is_student = True  # Boolean variable

# Variables can be reassigned
age = 26
print(f"{name} is {age} years old")
""",
        "why_it_works": "Python's interpreter allocates memory for the value and associates the variable name with that memory location. When you reassign, the name points to a new location.",
        "common_mistakes": [
            "Thinking variables must be declared before use (Python handles this automatically)",
            "Using = for comparison (use == instead)",
            "Creating variable names with spaces (use underscores instead)"
        ],
        "best_practices": [
            "Use descriptive variable names: user_age instead of ua",
            "Follow snake_case naming convention for variables",
            "Avoid single-letter names except for loops (i, j, k)"
        ]
    },
    
    "loops": {
        "level": SkillLevel.BEGINNER,
        "keywords": ["for", "while", "loop", "iterate", "range", "in"],
        "explanation": {
            "beginner": "A loop repeats a block of code multiple times. 'for' loops iterate through collections, 'while' loops continue until a condition is false.",
            "intermediate": "Loops are control flow structures. 'for' loops can iterate through iterables (lists, strings, ranges). 'while' loops are condition-based.",
            "advanced": "In Python, loops use the iterator protocol (__iter__, __next__). 'for' loops abstract iteration over any iterable object."
        },
        "code": """# For loop - iterate through a range
for i in range(5):
    print(i)  # Output: 0, 1, 2, 3, 4

# For loop - iterate through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# While loop - continue until condition is false
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1
""",
        "why_it_works": "For loops use Python's iterator protocol to go through each element. While loops check the condition before each iteration.",
        "common_mistakes": [
            "Off-by-one errors with range() - remember range(5) goes from 0-4, not 1-5",
            "Infinite loops from incorrect conditions",
            "Modifying a list while iterating through it"
        ],
        "best_practices": [
            "Use 'for' loops for iterating through collections (more Pythonic)",
            "Use 'while' loops only when you need condition-based iteration",
            "Use enumerate() if you need both index and value",
            "Avoid modifying collections during iteration"
        ]
    },
    
    "functions": {
        "level": SkillLevel.BEGINNER,
        "keywords": ["def", "function", "return", "parameter", "argument"],
        "explanation": {
            "beginner": "A function is a reusable block of code that performs a specific task. You define it with 'def' and call it by name with parentheses.",
            "intermediate": "Functions can take parameters (inputs) and return values (outputs). They help organize code and reduce repetition.",
            "advanced": "Functions are first-class objects in Python. They have a scope, can be passed as arguments, and support closures."
        },
        "code": """# Basic function definition
def greet(name):
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!

# Function with multiple parameters
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8

# Function with default parameters
def introduce(name, age=25):
    return f"{name} is {age} years old"

print(introduce("Bob"))  # Uses default age
print(introduce("Carol", 30))  # Overrides default
""",
        "why_it_works": "When you call a function, Python executes the code inside it with the provided arguments. The 'return' statement sends a value back.",
        "common_mistakes": [
            "Forgetting to return a value - function returns None by default",
            "Not understanding scope - variables inside functions are local",
            "Using mutable default arguments (like lists) - they persist across calls"
        ],
        "best_practices": [
            "One function should do one thing (Single Responsibility Principle)",
            "Use clear, descriptive function names",
            "Add docstrings to explain what functions do",
            "Avoid side effects - prefer returning values over modifying globals"
        ]
    },
    
    # INTERMEDIATE TOPICS
    "list_comprehension": {
        "level": SkillLevel.INTERMEDIATE,
        "keywords": ["comprehension", "[", "for", "if", "list", "create"],
        "explanation": {
            "beginner": "A list comprehension is a short way to create a new list by transforming or filtering an existing list.",
            "intermediate": "List comprehensions are more efficient and readable than using for loops to create lists. They have the form [expr for item in iterable if condition].",
            "advanced": "List comprehensions are syntactic sugar that compile to bytecode more efficiently than equivalent for loops. They create new scopes."
        },
        "code": """# Traditional way with a loop
numbers = [1, 2, 3, 4, 5]
squared = []
for num in numbers:
    squared.append(num ** 2)
print(squared)  # [1, 4, 9, 16, 25]

# List comprehension (cleaner!)
squared = [num ** 2 for num in numbers]
print(squared)  # [1, 4, 9, 16, 25]

# With condition - only even numbers
even_squared = [num ** 2 for num in numbers if num % 2 == 0]
print(even_squared)  # [4, 16]

# Nested comprehension
matrix = [[i * j for j in range(3)] for i in range(3)]
print(matrix)  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
""",
        "why_it_works": "List comprehensions are processed as a single expression by Python, making them faster and using less memory than loop-based list building.",
        "common_mistakes": [
            "Over-complicating comprehensions - keep them readable",
            "Using comprehensions for side effects instead of creating new lists",
            "Deeply nested comprehensions become hard to read"
        ],
        "best_practices": [
            "Use comprehensions for transformation and filtering",
            "If it takes more than 2 lines, use a regular loop instead",
            "Dictionary and set comprehensions exist too: {k: v for...} and {x for...}",
            "Add comments for complex comprehensions"
        ]
    },
    
    "dictionary": {
        "level": SkillLevel.INTERMEDIATE,
        "keywords": ["dict", "dictionary", "{}", "key", "value", "map"],
        "explanation": {
            "beginner": "A dictionary stores key-value pairs. You access values using their keys, not positions like in lists.",
            "intermediate": "Dictionaries are hash maps. Keys must be hashable (immutable), but values can be any type. They're unordered in Python < 3.7, ordered in 3.7+.",
            "advanced": "Dictionaries use hash tables for O(1) average-case lookup. Hash collisions are handled via chaining or open addressing."
        },
        "code": """# Creating a dictionary
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Accessing values
print(person["name"])  # Alice
print(person.get("age"))  # 25
print(person.get("job", "Not specified"))  # Not specified

# Adding/updating
person["job"] = "Engineer"
person["age"] = 26

# Iterating
for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
""",
        "why_it_works": "Dictionaries use hashing to store keys and their associated values. Python computes a hash for each key, allowing O(1) lookups.",
        "common_mistakes": [
            "Using mutable objects as keys (lists, dicts)",
            "KeyError from accessing non-existent keys - use .get() instead",
            "Assuming dictionary order before Python 3.7"
        ],
        "best_practices": [
            "Use .get() with default values instead of direct access",
            "Use strings for keys when possible",
            "Dictionary comprehensions for creating dicts programmatically",
            "Consider defaultdict or Counter for special use cases"
        ]
    },
    
    # ADVANCED TOPICS
    "decorators": {
        "level": SkillLevel.ADVANCED,
        "keywords": ["decorator", "@", "wrap", "function", "closure"],
        "explanation": {
            "beginner": "A decorator is a function that modifies another function or class without changing its source code.",
            "intermediate": "Decorators use closures to wrap functions. They're called with @ syntax and can add functionality before/after execution.",
            "advanced": "Decorators are higher-order functions that return wrapper functions with closures. They modify function behavior or metadata using functools."
        },
        "code": """import functools
from time import time

# Simple decorator
def uppercase_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@uppercase_decorator
def say_hello(name):
    return f"hello, {name}"

print(say_hello("alice"))  # HELLO, ALICE

# Decorator with parameters
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def get_data():
    return "data"

print(get_data())  # ['data', 'data', 'data']

# Practical: timing decorator
def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    import time
    time.sleep(0.5)
    return "Done"

slow_function()
""",
        "why_it_works": "Decorators use closures to capture the original function. The wrapper executes additional code before/after calling the original function.",
        "common_mistakes": [
            "Forgetting @functools.wraps - loses original function metadata",
            "Decorators that don't return a function",
            "Not handling *args/**kwargs - breaks functions with arguments"
        ],
        "best_practices": [
            "Always use @functools.wraps to preserve original function metadata",
            "Use *args, **kwargs to handle any function signature",
            "Keep decorators focused on a single concern",
            "Document what your decorator does clearly"
        ]
    },
    
    "async_await": {
        "level": SkillLevel.ADVANCED,
        "keywords": ["async", "await", "asyncio", "concurrent", "coroutine"],
        "explanation": {
            "beginner": "Async/await allows code to pause and resume, useful for I/O operations without blocking.",
            "intermediate": "Coroutines defined with 'async def' can be awaited. 'await' pauses execution until a coroutine completes.",
            "advanced": "Async uses event loops for cooperative multitasking. Multiple coroutines can run concurrently without threads."
        },
        "code": """import asyncio

# Basic async function
async def fetch_data(name):
    print(f"Fetching data for {name}...")
    await asyncio.sleep(1)  # Simulate I/O delay
    return f"Data for {name}"

# Running a single coroutine
async def main():
    result = await fetch_data("Alice")
    print(result)

asyncio.run(main())

# Running multiple coroutines concurrently
async def main_concurrent():
    results = await asyncio.gather(
        fetch_data("Alice"),
        fetch_data("Bob"),
        fetch_data("Charlie")
    )
    for result in results:
        print(result)

asyncio.run(main_concurrent())
""",
        "why_it_works": "Async functions are coroutines managed by an event loop. When await is called, control yields to the loop, allowing other coroutines to run.",
        "common_mistakes": [
            "Forgetting 'await' - coroutines don't execute without it",
            "Mixing sync and async code without proper bridges",
            "Blocking operations in async functions defeat the purpose"
        ],
        "best_practices": [
            "Use async for I/O-bound operations (network, file, database)",
            "Use threading/multiprocessing for CPU-bound work",
            "Test async code thoroughly - it has subtle timing issues",
            "Avoid blocking calls inside async functions"
        ]
    }
}

# Common Python concepts mapped to questions
QUESTION_PATTERNS = {
    "how do i create": "variables",
    "what is a variable": "variables",
    "how do i loop": "loops",
    "for loop": "loops",
    "while loop": "loops",
    "how do i write": "functions",
    "what is a function": "functions",
    "def": "functions",
    "list comprehension": "list_comprehension",
    "comprehension": "list_comprehension",
    "dictionary": "dictionary",
    "dict": "dictionary",
    "decorator": "decorators",
    "@": "decorators",
    "async": "async_await",
    "await": "async_await",
    "asyncio": "async_await"
}


def detect_skill_level(question: str) -> SkillLevel:
    """Detect user's likely skill level based on question"""
    question_lower = question.lower()
    
    beginner_keywords = ["what is", "how do i", "how to", "explain", "beginner", "basic", "simple"]
    advanced_keywords = ["optimization", "performance", "design pattern", "metaclass", "descriptor", "advanced"]
    
    if any(word in question_lower for word in advanced_keywords):
        return SkillLevel.ADVANCED
    
    if any(word in question_lower for word in beginner_keywords):
        return SkillLevel.BEGINNER
    
    return SkillLevel.INTERMEDIATE


def find_python_topic(question: str) -> str:
    """Find the Python topic being asked about"""
    question_lower = question.lower()
    
    # Check patterns first
    for pattern, topic in QUESTION_PATTERNS.items():
        if pattern in question_lower:
            return topic
    
    # Check exact keywords
    for topic, data in PYTHON_TOPICS.items():
        for keyword in data["keywords"]:
            if keyword.lower() in question_lower:
                return topic
    
    return None


def format_tutor_response(topic: str, skill_level: SkillLevel) -> str:
    """Format a complete Python tutoring response"""
    if topic not in PYTHON_TOPICS:
        return None
    
    topic_data = PYTHON_TOPICS[topic]
    
    # Select explanation based on skill level
    explanation_text = topic_data["explanation"].get(
        skill_level.value,
        topic_data["explanation"]["beginner"]
    )
    
    # Build response
    response = f"""
📌 **Quick Answer:**
{explanation_text}

💻 **Code Example:**
```python
{topic_data['code'].strip()}
```

🎯 **Why It Works:**
{topic_data['why_it_works']}

⚠️ **Common Mistakes to Avoid:**
"""
    
    for mistake in topic_data['common_mistakes']:
        response += f"\n• {mistake}"
    
    response += f"\n\n✨ **Best Practices:**"
    for practice in topic_data['best_practices']:
        response += f"\n• {practice}"
    
    response += f"\n\n🔑 **Key Takeaway:**"
    response += f"\nMastering '{topic}' is essential for Python programming. Practice with different scenarios and gradually explore more advanced patterns."
    
    return response


def get_python_tutor_response(question: str) -> Dict:
    """Main function to get tutoring response for Python questions"""
    
    # Detect skill level
    skill_level = detect_skill_level(question)
    
    # Find topic
    topic = find_python_topic(question)
    
    if not topic:
        return {
            "found": False,
            "message": "I couldn't identify a specific Python topic in your question. Try asking about: variables, loops, functions, list comprehensions, dictionaries, decorators, or async programming."
        }
    
    response = format_tutor_response(topic, skill_level)
    
    return {
        "found": True,
        "topic": topic,
        "skill_level": skill_level.value,
        "response": response,
        "type": "python_tutor"
    }

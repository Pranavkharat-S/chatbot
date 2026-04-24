"""
Test script to verify Python Tutor System integration
"""

from python_tutor import get_python_tutor_response, detect_skill_level

print("=" * 80)
print("PYTHON TUTOR SYSTEM - INTEGRATION TEST")
print("=" * 80)

test_questions = [
    ("What is a variable?", "variables"),
    ("How do I write a function?", "functions"),
    ("What is a list comprehension?", "list_comprehension"),
    ("Explain decorators", "decorators"),
    ("Tell me about async/await", "async_await"),
    ("What is a dictionary?", "dictionary"),
    ("How do for loops work?", "loops"),
    ("What is machine learning?", None),  # Should not match tutor
]

for question, expected_topic in test_questions:
    print(f"\n{'─' * 80}")
    print(f"Question: {question}")
    print(f"Expected Topic: {expected_topic}")
    print(f"{'─' * 80}")
    
    response = get_python_tutor_response(question)
    
    if response["found"]:
        print(f"✅ FOUND - Python Tutor Response")
        print(f"   Topic: {response['topic']}")
        print(f"   Skill Level: {response['skill_level']}")
        print(f"\n   Response Preview (first 200 chars):")
        print(f"   {response['response'][:200]}...")
        
        if expected_topic and response['topic'] == expected_topic:
            print(f"\n   ✅ CORRECT TOPIC IDENTIFIED")
        elif expected_topic:
            print(f"\n   ⚠️  Expected {expected_topic}, got {response['topic']}")
    else:
        print(f"❌ NOT FOUND - Would use Knowledge Base/Intent Classification")
        print(f"   Message: {response['message']}")
        
        if expected_topic is None:
            print(f"   ✅ CORRECT (not a Python topic question)")

print(f"\n{'=' * 80}")
print("SKILL LEVEL DETECTION TEST")
print(f"{'=' * 80}")

skill_tests = [
    ("What is a variable?", "BEGINNER"),
    ("How do I use decorators?", "BEGINNER"),
    ("Explain the decorator pattern in depth", "ADVANCED"),
    ("Can you optimize this code?", "INTERMEDIATE"),
    ("What is async programming?", "BEGINNER"),
]

for question, expected_level in skill_tests:
    detected = detect_skill_level(question)
    status = "✅" if detected.value.upper() == expected_level else "⚠️"
    print(f"\n{status} Question: {question}")
    print(f"   Expected: {expected_level} | Detected: {detected.value.upper()}")

print(f"\n{'=' * 80}")
print("✅ INTEGRATION TEST COMPLETE")
print(f"{'=' * 80}")
print("\nNext Steps:")
print("1. Run Flask app: python app.py")
print("2. Open browser: http://127.0.0.1:5000")
print("3. Try asking Python questions!")
print(f"{'=' * 80}")

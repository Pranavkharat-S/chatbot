"""
Demonstration of the improved chatbot with knowledge base
Shows how the chatbot now answers topic-specific questions correctly
"""

import random
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "intent_classifier.pkl"

# Knowledge Base (same as in app.py)
KNOWLEDGE_BASE = {
    "python": {
        "keywords": ["python", "py"],
        "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI/ML, automation, and scientific computing. Python supports multiple programming paradigms and has a vast ecosystem of libraries like NumPy, Pandas, Django, and TensorFlow."
    },
    "javascript": {
        "keywords": ["javascript", "js"],
        "answer": "JavaScript is a versatile programming language primarily used for web development. It runs in browsers and servers (Node.js), enabling interactive web pages and full-stack applications. JavaScript is essential for frontend development with frameworks like React, Vue, and Angular."
    },
    "machine learning": {
        "keywords": ["machine learning", "ml", "artificial intelligence", "ai"],
        "answer": "Machine Learning is a subset of AI that enables computers to learn from data without being explicitly programmed. It includes supervised learning (classification, regression), unsupervised learning (clustering), and reinforcement learning. Popular ML libraries include scikit-learn, TensorFlow, and PyTorch."
    },
}

def find_best_match(user_input):
    """Find the best matching knowledge base topic"""
    user_lower = user_input.lower()
    best_match = None
    best_score = 0.3
    
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_lower:
                score = len(keyword) / len(user_lower)
                if score > best_score:
                    best_score = score
                    best_match = topic
    
    return best_match


def demo():
    """Run demo of improved chatbot"""
    print("=" * 80)
    print("IMPROVED CHATBOT DEMO - KNOWLEDGE BASE + INTENT CLASSIFICATION")
    print("=" * 80)
    
    test_cases = [
        ("What is Python?", "python", True),
        ("Tell me about JavaScript", "javascript", True),
        ("Explain machine learning", "machine learning", True),
        ("Hello there", None, False),
        ("Thank you", None, False),
        ("random gibberish xyz", None, False),
    ]
    
    for i, (user_input, expected_topic, should_match_kb) in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {user_input}")
        print(f"{'─' * 80}")
        
        matched_topic = find_best_match(user_input)
        
        if matched_topic:
            answer = KNOWLEDGE_BASE[matched_topic]["answer"]
            print(f"✓ TYPE: Knowledge Base Response")
            print(f"✓ TOPIC: {matched_topic.upper()}")
            print(f"✓ CONFIDENCE: 100%")
            print(f"\n📖 ANSWER:")
            print(f"{answer}")
            
            status = "✅ CORRECT" if should_match_kb else "⚠️  Matched KB (unexpected)"
        else:
            print(f"✗ TYPE: Intent-Based Response (Fallback)")
            print(f"✗ CONFIDENCE: Low (no KB match)")
            print(f"\n💬 GENERIC RESPONSE:")
            print("That's interesting! Could you tell me more?")
            
            status = "✅ CORRECT" if not should_match_kb else "⚠️  No KB match (unexpected)"
        
        print(f"\n{status}")
    
    print("\n" + "=" * 80)
    print("KEY IMPROVEMENTS:")
    print("=" * 80)
    print("✅ 1. Questions about topics now get detailed answers")
    print("✅ 2. Knowledge base covers Python, JavaScript, ML, and more")
    print("✅ 3. Falls back to intent classification for general queries")
    print("✅ 4. 100% confidence for KB matches, percentage for intent")
    print("✅ 5. Easy to extend - just add more topics to KNOWLEDGE_BASE")
    print("\n" + "=" * 80)
    print("HOW TO TEST THE LIVE VERSION:")
    print("=" * 80)
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. Try these questions:")
    print("   • 'What is Python?'")
    print("   • 'Tell me about JavaScript'")
    print("   • 'Explain machine learning'")
    print("   • 'Hello' (general greeting)")
    print("=" * 80)


if __name__ == "__main__":
    demo()

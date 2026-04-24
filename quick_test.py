"""
Quick ML Model Training and Testing (Non-interactive)
"""

import pickle
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Model paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
INTENT_MODEL_PATH = MODEL_DIR / "intent_classifier.pkl"

# Training data
TRAINING_DATA = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "howdy"],
    "farewell": ["bye", "goodbye", "see you", "farewell", "catch you later"],
    "help": ["help", "assist me", "i need help", "support", "guide me"],
    "thanks": ["thank you", "thanks", "appreciate it", "much appreciated"],
    "about": ["who are you", "what are you", "your purpose", "describe yourself"],
    "weather": ["weather", "is it raining", "forecast", "temperature"],
    "time": ["what time is it", "current time", "tell me the time"],
}

RESPONSES = {
    "greeting": "Hello! How can I help?",
    "farewell": "Goodbye! Have a great day!",
    "help": "I'm here to help! What do you need?",
    "thanks": "You're welcome!",
    "about": "I'm an AI chatbot with ML capabilities!",
    "weather": "Check a weather service for current conditions.",
    "time": "Check your system clock.",
    "default": "That's interesting! Tell me more."
}


def train_model():
    """Train the intent classification model"""
    print("=" * 60)
    print("TRAINING ML CHATBOT MODEL")
    print("=" * 60)
    
    # Prepare training data
    texts = []
    labels = []
    
    for intent, phrases in TRAINING_DATA.items():
        for phrase in phrases:
            texts.append(phrase)
            labels.append(intent)
    
    print(f"\n✓ Dataset prepared:")
    print(f"  - Total samples: {len(texts)}")
    print(f"  - Intents: {', '.join(TRAINING_DATA.keys())}")
    
    # Train model
    model = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, max_features=100)),
        ('clf', MultinomialNB())
    ])
    
    model.fit(texts, labels)
    
    # Save model
    MODEL_DIR.mkdir(exist_ok=True)
    with open(INTENT_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n✓ Model trained and saved!")
    print(f"  Location: {INTENT_MODEL_PATH}")
    
    return model


def load_or_train():
    """Load existing model or train new one"""
    if INTENT_MODEL_PATH.exists():
        print("✓ Loading pre-trained model...")
        with open(INTENT_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("  Model loaded successfully!\n")
        return model
    else:
        print("⚡ No model found. Training new model...\n")
        return train_model()


def test_model(model):
    """Test the model with examples"""
    print("\n" + "=" * 60)
    print("TESTING CHATBOT")
    print("=" * 60)
    
    test_cases = [
        "hello there",
        "goodbye friend",
        "can you assist me",
        "thank you very much",
        "who are you",
        "weather forecast",
        "what is the time",
        "random gibberish xyz abc",
    ]
    
    for user_input in test_cases:
        intent = model.predict([user_input.lower()])[0]
        confidence = max(model.predict_proba([user_input.lower()])[0])
        response = RESPONSES.get(intent, RESPONSES["default"])
        
        print(f"\n📝 Input: {user_input}")
        print(f"🎯 Intent: {intent} ({confidence:.1%} confidence)")
        print(f"💬 Response: {response}")


if __name__ == '__main__':
    model = load_or_train()
    test_model(model)
    print("\n" + "=" * 60)
    print("✅ ML Chatbot is ready!")
    print("=" * 60)

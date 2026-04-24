"""
Standalone ML Chatbot Trainer and Tester
Tests the ML model without needing Wechaty connection
"""

import json
import pickle
from pathlib import Path
from typing import Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Model paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
INTENT_MODEL_PATH = MODEL_DIR / "intent_classifier.pkl"

# Training data with more examples
TRAINING_DATA = {
    "greeting": [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon",
        "good evening", "howdy", "what's up", "hiya", "hello there", "hi mate"
    ],
    "farewell": [
        "bye", "goodbye", "see you", "see you later", "farewell", "catch you later",
        "goodbye", "till then", "take care", "cya", "bye bye"
    ],
    "help": [
        "help", "assist me", "i need help", "can you help", "support", "need assistance",
        "how do i", "how to", "guide me", "teach me", "help me", "assist"
    ],
    "thanks": [
        "thank you", "thanks", "thank you so much", "appreciate it", "thanks a lot",
        "much appreciated", "thank you very much", "ta", "cheers", "thanks mate"
    ],
    "about": [
        "who are you", "what are you", "tell me about yourself", "who is this",
        "what can you do", "your purpose", "describe yourself", "info about you"
    ],
    "weather": [
        "weather", "is it raining", "is it sunny", "temperature", "forecast",
        "how is the weather", "what's the weather like", "weather report"
    ],
    "time": [
        "what time is it", "current time", "tell me the time", "time please",
        "what's the time", "current hour"
    ]
}

RESPONSES = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Greetings! How may I help?"
    ],
    "farewell": [
        "Goodbye! It was nice chatting with you!",
        "See you later! Take care!",
        "Bye! Have a great day!"
    ],
    "help": [
        "I'm here to help! What do you need assistance with?",
        "Sure, I can help! What's your question?",
        "Of course! Tell me what you need."
    ],
    "thanks": [
        "You're welcome!",
        "My pleasure!",
        "Happy to help!"
    ],
    "about": [
        "I'm an AI chatbot with machine learning capabilities.",
        "I'm a smart chatbot powered by ML. I can understand intents!",
        "I'm an intelligent assistant designed to help you."
    ],
    "weather": [
        "I don't have real-time weather data. Check a weather website!",
        "For weather info, check a weather service online."
    ],
    "time": [
        "Check your system clock for the current time.",
        "Please check your device's time display."
    ],
    "default": [
        "That's interesting! Could you tell me more?",
        "I'm not sure I understand. Could you rephrase?",
        "Tell me more about it!",
        "Can you explain further?"
    ]
}


class MLChatbotTrainer:
    """Train, save, and test the intent classification model"""
    
    def __init__(self):
        self.model = None
        self.intent_labels = list(TRAINING_DATA.keys())
    
    def train_model(self):
        """Train the intent classification model"""
        print("\n" + "="*60)
        print("TRAINING ML CHATBOT MODEL")
        print("="*60)
        
        # Prepare training data
        texts = []
        labels = []
        
        for intent, phrases in TRAINING_DATA.items():
            for phrase in phrases:
                texts.append(phrase)
                labels.append(intent)
        
        print(f"\n📊 Dataset Statistics:")
        print(f"   Total samples: {len(texts)}")
        print(f"   Number of intents: {len(self.intent_labels)}")
        for intent in self.intent_labels:
            count = len(TRAINING_DATA[intent])
            print(f"   - {intent}: {count} samples")
        
        # Create and train pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, max_features=100)),
            ('clf', MultinomialNB())
        ])
        
        # Split data for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"\n✅ Model Training Complete!")
        print(f"   Training Accuracy: {train_score:.2%}")
        print(f"   Testing Accuracy: {test_score:.2%}")
        
        return True
    
    def save_model(self):
        """Save the trained model"""
        MODEL_DIR.mkdir(exist_ok=True)
        with open(INTENT_MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"\n💾 Model saved to: {INTENT_MODEL_PATH}")
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent and return confidence"""
        prediction = self.model.predict([text.lower()])
        confidence = max(self.model.predict_proba([text.lower()])[0])
        return prediction[0], confidence
    
    def test_with_examples(self):
        """Test the model with example inputs"""
        print("\n" + "="*60)
        print("TESTING CHATBOT WITH EXAMPLE INPUTS")
        print("="*60)
        
        test_inputs = [
            "hello there",
            "goodbye my friend",
            "can you help me",
            "thank you so much",
            "who are you",
            "what's the weather",
            "tell me the time",
            "random text that makes no sense xyz",
        ]
        
        for user_input in test_inputs:
            intent, confidence = self.classify_intent(user_input)
            response = np.random.choice(RESPONSES.get(intent, RESPONSES["default"]))
            print(f"\n👤 User: {user_input}")
            print(f"🤖 Intent: {intent} (confidence: {confidence:.2%})")
            print(f"   Response: {response}")
    
    def interactive_chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("INTERACTIVE CHAT MODE")
        print("="*60)
        print("Type 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            intent, confidence = self.classify_intent(user_input)
            response = np.random.choice(RESPONSES.get(intent, RESPONSES["default"]))
            
            print(f"Bot: {response}")
            print(f"     [Intent: {intent}, Confidence: {confidence:.2%}]\n")


def main():
    """Main execution"""
    trainer = MLChatbotTrainer()
    
    # Check if model exists
    if INTENT_MODEL_PATH.exists():
        print("\n✓ Pre-trained model found!")
        with open(INTENT_MODEL_PATH, 'rb') as f:
            trainer.model = pickle.load(f)
        print("Model loaded successfully!")
    else:
        print("\n⚡ No pre-trained model found. Training new model...")
        trainer.train_model()
        trainer.save_model()
    
    # Run tests
    trainer.test_with_examples()
    
    # Interactive mode
    print("\n" + "="*60)
    try:
        trainer.interactive_chat()
    except KeyboardInterrupt:
        print("\n\nChat terminated. Goodbye!")


if __name__ == '__main__':
    main()

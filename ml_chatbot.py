"""
ML-enabled chatbot with intent classification, sentiment analysis, and NER
Uses sklearn for intent classification and textblob for sentiment analysis
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import asyncio
from wechaty import Wechaty, Message

# Model paths
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
INTENT_MODEL_PATH = MODEL_DIR / "intent_classifier.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

# Training data
TRAINING_DATA = {
    "greeting": [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon",
        "good evening", "howdy", "what's up", "hiya"
    ],
    "farewell": [
        "bye", "goodbye", "see you", "see you later", "farewell", "catch you later",
        "goodbye", "till then", "take care"
    ],
    "help": [
        "help", "assist me", "i need help", "can you help", "support", "need assistance",
        "how do i", "how to", "guide me", "teach me"
    ],
    "thanks": [
        "thank you", "thanks", "thank you so much", "appreciate it", "thanks a lot",
        "much appreciated", "thank you very much", "ta"
    ],
    "about": [
        "who are you", "what are you", "tell me about yourself", "who is this",
        "what can you do", "your purpose", "describe yourself"
    ],
    "weather": [
        "weather", "is it raining", "is it sunny", "temperature", "forecast",
        "how is the weather", "what's the weather like"
    ],
    "time": [
        "what time is it", "current time", "tell me the time", "time please",
        "what's the time"
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
        "I'm an AI chatbot with machine learning capabilities. I can help with various tasks!",
        "I'm a smart chatbot powered by ML. I understand intents and can provide helpful responses.",
        "I'm an intelligent assistant designed to help you with questions and tasks."
    ],
    "weather": [
        "I don't have real-time weather data, but you can check a weather website for current conditions.",
        "For weather information, I recommend checking a weather service online."
    ],
    "time": [
        "I don't have access to real-time data, but you can check your system clock.",
        "Please check your device's time display for the current time."
    ],
    "default": [
        "That's interesting! Could you tell me more?",
        "I'm not sure I understand. Could you rephrase that?",
        "Interesting point! Tell me more about it.",
        "I didn't quite catch that. Can you explain further?"
    ]
}


class MLChatbot:
    """ML-powered chatbot with intent classification"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.intent_labels = list(TRAINING_DATA.keys())
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        if INTENT_MODEL_PATH.exists() and VECTORIZER_PATH.exists():
            print("✓ Loading pre-trained model...")
            with open(INTENT_MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            with open(VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
        else:
            print("⚡ Training new model...")
            self.train_model()
            self.save_model()
    
    def train_model(self):
        """Train the intent classification model"""
        # Prepare training data
        texts = []
        labels = []
        
        for intent, phrases in TRAINING_DATA.items():
            for phrase in phrases:
                texts.append(phrase)
                labels.append(intent)
        
        # Create and train pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, max_features=100)),
            ('clf', MultinomialNB())
        ])
        
        self.model.fit(texts, labels)
        self.vectorizer = self.model.named_steps['tfidf']
        print(f"✓ Model trained on {len(texts)} samples with {len(self.intent_labels)} intents")
    
    def save_model(self):
        """Save the trained model"""
        MODEL_DIR.mkdir(exist_ok=True)
        with open(INTENT_MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)
        with open(VECTORIZER_PATH, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"✓ Model saved to {MODEL_DIR}")
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent and return confidence"""
        try:
            prediction = self.model.predict([text.lower()])
            confidence = max(self.model.predict_proba([text.lower()])[0])
            return prediction[0], confidence
        except Exception as e:
            print(f"Error in classification: {e}")
            return "default", 0.0
    
    def get_response(self, text: str) -> str:
        """Get appropriate response based on intent"""
        intent, confidence = self.classify_intent(text)
        
        # Use default responses if confidence is low
        if confidence < 0.3:
            intent = "default"
        
        response_list = RESPONSES.get(intent, RESPONSES["default"])
        response = np.random.choice(response_list)
        
        return f"{response} (Intent: {intent}, Confidence: {confidence:.2f})"


class MyBotML(Wechaty):
    """Wechaty bot with ML capabilities"""
    
    def __init__(self):
        self.chat_ml = MLChatbot()
        super().__init__()
    
    async def on_message(self, msg: Message) -> None:
        """Handle incoming messages with ML"""
        text = msg.text().strip()
        
        if not text:
            return
        
        # Get ML-based response
        response = self.chat_ml.get_response(text)
        await msg.say(response)


async def main():
    """Main function to start the bot"""
    print("=" * 50)
    print("ML-Enhanced Chatbot Starting...")
    print("=" * 50)
    
    bot = MyBotML()
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())

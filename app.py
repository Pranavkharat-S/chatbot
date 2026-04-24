import json
import pickle
import random
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from python_tutor import get_python_tutor_response

app = Flask(__name__)

MODEL_PATH = Path(__file__).parent / "models" / "intent_classifier.pkl"
QA_DATASET_PATH = Path(__file__).parent / "python_qa_dataset.json"
QA_MATCH_THRESHOLD = 0.4

TRAINING_DATA = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy", "what's up", "hiya", "hello there", "hi mate"],
    "farewell": ["bye", "goodbye", "see you", "see you later", "farewell", "catch you later", "till then", "take care", "cya", "bye bye"],
    "help": ["help", "assist me", "i need help", "can you help", "support", "need assistance", "how do i", "how to", "guide me", "teach me", "help me", "assist"],
    "thanks": ["thank you", "thanks", "thank you so much", "appreciate it", "thanks a lot", "much appreciated", "thank you very much", "ta", "cheers", "thanks mate"],
    "about": ["who are you", "what are you", "tell me about yourself", "who is this", "what can you do", "your purpose", "describe yourself", "info about you"],
    "weather": ["weather", "is it raining", "is it sunny", "temperature", "forecast", "how is the weather", "what's the weather like", "weather report"],
    "time": ["what time is it", "current time", "tell me the time", "time please", "what's the time", "current hour"],
}

RESPONSES = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! How may I help?"],
    "farewell": ["Goodbye! It was nice chatting with you!", "See you later! Take care!", "Bye! Have a great day!"],
    "help": ["I'm here to help! What do you need assistance with?", "Sure, I can help! What's your question?", "Of course! Tell me what you need."],
    "thanks": ["You're welcome!", "My pleasure!", "Happy to help!"],
    "about": ["I'm an AI chatbot with machine learning capabilities.", "I'm a smart chatbot powered by ML. I can understand intents!", "I'm an intelligent assistant designed to help you."],
    "weather": ["I don't have real-time weather data. Check a weather website!", "For weather info, check a weather service online."],
    "time": ["Check your system clock for the current time.", "Please check your device's time display."],
    "default": ["That's interesting! Could you tell me more?", "I'm not sure I understand. Could you rephrase?", "Tell me more about it!", "Can you explain further?"],
}

# Knowledge Base with Topic-specific Answers
KNOWLEDGE_BASE = {
    # Programming Languages
    "python": {
        "keywords": ["python", "py"],
        "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI/ML, automation, and scientific computing. Python supports multiple programming paradigms and has a vast ecosystem of libraries like NumPy, Pandas, Django, and TensorFlow."
    },
    "javascript": {
        "keywords": ["javascript", "js"],
        "answer": "JavaScript is a versatile programming language primarily used for web development. It runs in browsers and servers (Node.js), enabling interactive web pages and full-stack applications. JavaScript is essential for frontend development with frameworks like React, Vue, and Angular."
    },
    "java": {
        "keywords": ["java"],
        "answer": "Java is an object-oriented, compiled programming language known for 'write once, run anywhere'. It's widely used in enterprise applications, Android development, and large-scale systems. Java emphasizes strong typing, memory management, and robustness."
    },
    "c++": {
        "keywords": ["c++", "cpp"],
        "answer": "C++ is a powerful compiled language used for system software, game development, and performance-critical applications. It combines low-level memory manipulation with high-level object-oriented features, making it ideal for resource-intensive programs."
    },
    
    # Machine Learning
    "machine learning": {
        "keywords": ["machine learning", "ml", "artificial intelligence", "ai", "neural network", "deep learning"],
        "answer": "Machine Learning is a subset of AI that enables computers to learn from data without being explicitly programmed. It includes supervised learning (classification, regression), unsupervised learning (clustering), and reinforcement learning. Popular ML libraries include scikit-learn, TensorFlow, and PyTorch."
    },
    
    # Web Development
    "web development": {
        "keywords": ["web", "website", "html", "css", "frontend", "backend"],
        "answer": "Web development involves building websites and web applications using HTML (structure), CSS (styling), and JavaScript (interactivity). It includes frontend (client-side) and backend (server-side) development. Common frameworks include React, Vue, Django, Flask, and Node.js."
    },
    
    # Data Science
    "data science": {
        "keywords": ["data science", "data analysis", "analytics", "pandas", "numpy"],
        "answer": "Data Science combines statistics, programming, and domain expertise to extract insights from data. It involves data collection, cleaning, analysis, and visualization. Key tools include Python (Pandas, NumPy), R, SQL, and visualization libraries like Matplotlib and Seaborn."
    },
    
    # Databases
    "database": {
        "keywords": ["database", "sql", "mysql", "postgresql", "mongodb", "nosql"],
        "answer": "Databases store and manage structured or unstructured data. SQL databases (MySQL, PostgreSQL) use tables and are ACID-compliant. NoSQL databases (MongoDB, Redis) offer flexible schemas. Database design, indexing, and queries are crucial for application performance."
    },
    
    # General IT
    "programming": {
        "keywords": ["programming", "code", "coding", "software"],
        "answer": "Programming is the process of writing instructions (code) that computers execute. It involves problem-solving, logic, algorithms, and data structures. Good programmers focus on clean code, testing, debugging, and continuous learning."
    },
    "algorithm": {
        "keywords": ["algorithm", "algorithms"],
        "answer": "An algorithm is a step-by-step procedure to solve a problem or complete a task. In computing, algorithms define how data is processed. Common algorithms include sorting (Quick Sort, Merge Sort), searching (Binary Search), and graph traversal (DFS, BFS)."
    },
}

KNOWLEDGE_BASE_PATTERNS = {
    "who developed python": "python_creator",
    "who created python": "python_creator",
    "creator of python": "python_creator",
    "who made python": "python_creator",
    "when was python created": "python_history",
    "when did python start": "python_history",
    "what is python": "python",
    "describe python": "python",
    "define python": "python",
    "what is machine learning": "machine learning",
    "tell me about machine learning": "machine learning",
    "what is web development": "web development",
    "tell me about web development": "web development",
}

KNOWLEDGE_BASE_EXTRA = {
    "python_creator": {
        "keywords": ["who developed python", "who created python", "creator of python", "who made python"],
        "answer": "Python was created by Guido van Rossum in the late 1980s and first released in 1991. He designed Python with readability and ease of use in mind, hoping to make programming more approachable."
    },
    "python_history": {
        "keywords": ["when was python", "when did python", "python released"],
        "answer": "Python was first released in 1991 by Guido van Rossum. It evolved through major versions such as Python 2.x and Python 3.x, with Python 3 becoming the standard due to improved language features and compatibility."
    }
}


def load_or_train():
    if MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    texts, labels = [], []
    for intent, phrases in TRAINING_DATA.items():
        for phrase in phrases:
            texts.append(phrase)
            labels.append(intent)
    model = Pipeline([("tfidf", TfidfVectorizer(lowercase=True, max_features=100)), ("clf", MultinomialNB())])
    model.fit(texts, labels)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    return model


def load_qa_dataset():
    if not QA_DATASET_PATH.exists():
        return None, None, [], []
    with open(QA_DATASET_PATH, "r", encoding="utf-8") as f:
        qa_list = json.load(f)
    questions = [item["question"] for item in qa_list]
    answers = [item["answer"] for item in qa_list]
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", max_features=500)
    question_vectors = vectorizer.fit_transform(questions)
    return vectorizer, question_vectors, questions, answers


def find_qa_answer(user_input):
    if qa_vectorizer is None or qa_question_vectors is None:
        return None
    input_vec = qa_vectorizer.transform([user_input])
    similarities = cosine_similarity(input_vec, qa_question_vectors)[0]
    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])
    if best_score >= QA_MATCH_THRESHOLD:
        return qa_answers[best_index]
    return None


def find_best_match(user_input):
    """Find the best matching knowledge base topic"""
    user_lower = user_input.lower()

    # Exact pattern matching first for more precise answers
    for pattern, topic in KNOWLEDGE_BASE_PATTERNS.items():
        if pattern in user_lower:
            return topic

    # Check extra topic mappings that may not be in the main KB
    for topic, data in KNOWLEDGE_BASE_EXTRA.items():
        for keyword in data["keywords"]:
            if keyword in user_lower:
                return topic

    # Fallback to keyword-based matching
    best_match = None
    best_score = 0.3  # Minimum threshold
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_lower:
                score = len(keyword) / len(user_lower)
                if score > best_score:
                    best_score = score
                    best_match = topic
    
    return best_match


def extract_question_type(user_input):
    """Determine if user is asking 'what', 'how', 'why', etc."""
    user_lower = user_input.lower()
    if any(word in user_lower for word in ["what", "what's", "explain", "define", "tell me"]):
        return "definition"
    elif any(word in user_lower for word in ["how", "how to", "can you", "way to"]):
        return "howto"
    elif any(word in user_lower for word in ["why"]):
        return "reason"
    return "general"


model = load_or_train()
qa_vectorizer, qa_question_vectors, qa_questions, qa_answers = load_qa_dataset()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please say something!"})
    
    # Step 1: Try the trained QA dataset
    qa_answer = find_qa_answer(user_input)
    if qa_answer:
        return jsonify({
            "response": qa_answer,
            "intent": "qa_dataset",
            "topic": "dataset_answer",
            "confidence": "100%",
            "type": "qa_dataset"
        })

    # Step 2: Check if it's a Python question - use AI tutor
    python_response = get_python_tutor_response(user_input)
    if python_response["found"]:
        return jsonify({
            "response": python_response["response"],
            "intent": "python_tutor",
            "topic": python_response["topic"],
            "skill_level": python_response["skill_level"],
            "confidence": "95%",
            "type": "python_tutor"
        })
    
    # Step 3: Try to find answer in knowledge base
    matched_topic = find_best_match(user_input)
    if matched_topic:
        if matched_topic in KNOWLEDGE_BASE:
            answer = KNOWLEDGE_BASE[matched_topic]["answer"]
        elif matched_topic in KNOWLEDGE_BASE_EXTRA:
            answer = KNOWLEDGE_BASE_EXTRA[matched_topic]["answer"]
        else:
            answer = "I'm not sure about that exact question, but I can help with Python topics."
        return jsonify({
            "response": answer,
            "intent": "knowledge",
            "topic": matched_topic,
            "confidence": "100%",
            "type": "knowledge_base"
        })
    
    # Step 3: Fall back to intent classification for general queries
    intent = model.predict([user_input.lower()])[0]
    confidence = max(model.predict_proba([user_input.lower()])[0])
    response = random.choice(RESPONSES.get(intent, RESPONSES["default"]))
    
    return jsonify({
        "response": response,
        "intent": intent,
        "confidence": f"{confidence:.1%}",
        "type": "intent_based"
    })


if __name__ == "__main__":
    app.run(debug=True)

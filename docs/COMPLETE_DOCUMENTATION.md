# Chatbot Project - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Architecture](#project-architecture)
3. [Installation & Setup](#installation--setup)
4. [Project Structure](#project-structure)
5. [Components](#components)
6. [API Documentation](#api-documentation)
7. [Usage Guide](#usage-guide)
8. [Development Guide](#development-guide)
9. [Features](#features)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

### What is This Project?

The **Smart Chatbot with Python Tutor** is a hybrid AI-powered conversational agent that combines multiple AI techniques:

- **Intent-Based Classification**: Uses Machine Learning (Naive Bayes + TF-IDF) to understand user intent
- **Python Tutoring**: Provides educational explanations for Python concepts at multiple skill levels
- **Knowledge Base Q&A**: Answers questions about programming, web development, data science, and more
- **Web Interface**: User-friendly Flask web application with real-time chat

### Project Goals

✅ Provide an intelligent chatbot that understands user intent  
✅ Offer Python tutoring at beginner, intermediate, and advanced levels  
✅ Maintain a comprehensive knowledge base for programming topics  
✅ Demonstrate ML model training and inference  
✅ Create an educational platform for learning  

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask (Python) |
| **ML Library** | scikit-learn |
| **NLP** | TF-IDF Vectorization |
| **ML Algorithm** | Naive Bayes Classifier |
| **Frontend** | HTML5 + CSS3 + JavaScript |
| **Database** | JSON (python_qa_dataset.json) |
| **Model Serialization** | Pickle |

---

## Project Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Web Interface (UI)                     │
│              (templates/index.html)                      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Flask Backend (src/app.py)                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Route Handlers:                                  │   │
│  │ - POST /chat -> Process message                 │   │
│  │ - GET /  -> Serve HTML                         │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌─────────┐ ┌──────────┐ ┌────────────┐
    │   ML    │ │ Python   │ │ Knowledge  │
    │ Intent  │ │  Tutor   │ │   Base     │
    │ Module  │ │ Module   │ │  Module    │
    └─────────┘ └──────────┘ └────────────┘

ML Model (intent_classifier.pkl)
    │
    └─> Predicts user intent (greeting, farewell, help, etc.)
```

### Data Flow

```
User Input
    │
    ▼
Intent Classifier (ML Model)
    │
    ├─ If Python topic detected
    │   ▼
    │   Python Tutor Module
    │   │
    │   ├─ Extract topic
    │   ├─ Determine skill level (beginner/intermediate/advanced)
    │   └─ Return educated response with code examples
    │
    ├─ If general programming topic
    │   ▼
    │   Knowledge Base Lookup
    │   │
    │   ├─ Search keywords
    │   └─ Return knowledge answer
    │
    └─ If general intent (greeting, farewell, etc.)
        ▼
        Intent Response
        └─ Return predefined response

    ▼
Format Response + Metadata
    │
    ▼
Send JSON to Frontend
    │
    ▼
Display in Chat UI
```

---

## Installation & Setup

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Pranavkharat-S/chatbot.git
cd chatbot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies Installed:**

```
wechaty          - Wechaty bot framework (optional, for advanced features)
scikit-learn     - Machine learning library
numpy            - Numerical computing
textblob         - Text processing
flask            - Web framework
```

### Step 3: Verify Installation

```bash
python -c "import flask, sklearn, numpy; print('✅ All dependencies installed!')"
```

### Step 4: Run the Application

```bash
python src/app.py
```

**Expected Output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: off
Press CTRL+C to quit
```

### Step 5: Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

## Project Structure

### Directory Layout

```
chatbot/
│
├── 📂 src/                          # Source Code
│   ├── app.py                       # Main Flask application
│   └── python_tutor.py              # Python tutoring module
│
├── 📂 models/                       # Machine Learning Models
│   └── intent_classifier.pkl        # Trained ML model (Naive Bayes)
│
├── 📂 templates/                    # Web Frontend
│   └── index.html                   # Chat interface
│
├── 📂 docs/                         # Documentation
│   ├── BEGINNER_GUIDE.md            # Beginner-friendly guide
│   └── COMPLETE_DOCUMENTATION.md    # This file
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project README
├── START_HERE.txt                   # Quick start guide
└── PROJECT_STRUCTURE.md             # Structure overview
```

### Key File Descriptions

| File | Purpose | Size |
|------|---------|------|
| `src/app.py` | Flask app, routes, ML model, knowledge base | ~400 lines |
| `src/python_tutor.py` | Python education module, tutoring logic | ~200+ lines |
| `templates/index.html` | Web UI, chat interface | ~300 lines |
| `models/intent_classifier.pkl` | Trained Naive Bayes model | ~50KB |
| `requirements.txt` | Package dependencies | 5 lines |

---

## Components

### 1. Flask Application (`src/app.py`)

#### Purpose
Main application server handling HTTP requests, ML inference, and response generation.

#### Key Functions

| Function | Description |
|----------|-------------|
| `app.route('/')` | Serves the HTML interface |
| `app.route('/chat', methods=['POST'])` | Processes user messages |
| `predict_intent(text)` | Uses ML model to classify intent |
| `get_knowledge_response(topic)` | Looks up knowledge base |
| `process_message(user_input)` | Orchestrates message processing |

#### Knowledge Base Structure

The app contains a comprehensive knowledge base organized by topics:

```python
KNOWLEDGE_BASE = {
    "python": {...},
    "javascript": {...},
    "machine learning": {...},
    "web development": {...},
    "data science": {...},
    # ... more topics
}
```

Each topic has:
- **keywords**: Search terms
- **answer**: Detailed explanation

#### Intent Classification

**Training Data (7 intents):**
- `greeting`: "hello", "hi", "hey", etc.
- `farewell`: "bye", "goodbye", "see you", etc.
- `help`: "help", "assist", "teach me", etc.
- `thanks`: "thank you", "thanks", "appreciate", etc.
- `about`: "who are you", "what can you do", etc.
- `weather`: "weather", "temperature", "forecast", etc.
- `time`: "what time", "current time", etc.

**Response Examples:**

```python
RESPONSES = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Greetings! How may I help?"
    ],
    # ... more intents
}
```

### 2. Python Tutor Module (`src/python_tutor.py`)

#### Purpose
Provides progressive Python education at multiple skill levels.

#### Supported Topics

**Beginner Level:**
- Variables
- Loops (for, while)
- Functions
- Basic data types

**Intermediate Level:**
- List comprehensions
- Decorators (basic)
- File handling
- Exception handling

**Advanced Level:**
- Async/await
- Memory management
- Meta-programming
- Advanced decorators

#### Response Structure

Each topic includes:

```python
{
    "level": SkillLevel.BEGINNER,
    "keywords": ["variable", "var", "declare"],
    "explanation": {
        "beginner": "Simple explanation",
        "intermediate": "More detailed explanation",
        "advanced": "Deep technical explanation"
    },
    "code": "Python code example",
    "why_it_works": "How the code works",
    "common_mistakes": ["Mistake 1", "Mistake 2"],
    "best_practices": ["Practice 1", "Practice 2"]
}
```

### 3. Web Interface (`templates/index.html`)

#### Purpose
Provides user-friendly chat interface for interacting with the chatbot.

#### Features

- **Real-time Chat**: Send and receive messages
- **Markdown Support**: Formatted responses with code syntax highlighting
- **Responsive Design**: Works on desktop and mobile
- **Beautiful UI**: Gradient backgrounds, smooth animations
- **Code Highlighting**: Syntax highlighting for Python code examples

#### HTML Structure

```html
<div id="chat-container">
    <div id="header">🤖 Smart Chatbot + 🐍 Python Tutor</div>
    <div id="messages"><!-- Chat messages appear here --></div>
    <div id="input-area"><!-- User input field --></div>
</div>
```

#### CSS Highlights

- Modern gradient design (purple/blue)
- Mobile-responsive layout
- Smooth animations and transitions
- Syntax highlighting for code blocks

#### JavaScript Features

- Message parsing (Markdown to HTML)
- Auto-scroll to latest message
- Enter key to send message
- Real-time response rendering

---

## API Documentation

### Backend API

#### Endpoint: `/chat`

**Method:** POST

**Request Body:**
```json
{
    "message": "What is a list comprehension?"
}
```

**Response Structure:**
```json
{
    "response": "A list comprehension is a concise way to create lists...",
    "type": "python_tutor",
    "metadata": {
        "topic": "list comprehensions",
        "skill_level": "intermediate",
        "includes_code": true
    }
}
```

**Response Types:**
- `python_tutor`: Python education response
- `knowledge_base`: General programming knowledge
- `intent_response`: Intent-based response (greeting, farewell, etc.)

#### Example Requests & Responses

**Request 1: Python Topic**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do decorators work?"}'
```

**Response:**
```json
{
    "response": "Decorators are functions that modify other functions...",
    "type": "python_tutor",
    "metadata": {
        "topic": "decorators",
        "skill_level": "advanced"
    }
}
```

**Request 2: Greeting**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

**Response:**
```json
{
    "response": "Hello! How can I assist you today?",
    "type": "intent_response",
    "metadata": {
        "intent": "greeting"
    }
}
```

---

## Usage Guide

### Basic Usage

#### Starting the Application

```bash
python src/app.py
```

Navigate to `http://127.0.0.1:5000`

#### Asking Questions

**Type:** General Chat
```
You: Hello!
Bot: Hi there! What can I do for you?
```

**Type:** Python Tutoring
```
You: What is a variable?
Bot: [Comprehensive explanation at skill level]
```

**Type:** Knowledge Base
```
You: Tell me about machine learning
Bot: [Detailed ML explanation with examples]
```

### Example Conversations

#### Example 1: Learn Python Variables

```
User: What is a variable?
Bot: A variable is a named container that stores a value in memory...
     [Provides beginner explanation with code example]

User: Tell me more about variables
Bot: [Switches to intermediate level, more technical details]
```

#### Example 2: General Programming Question

```
User: What is web development?
Bot: Web development involves building websites and web applications...
     [Returns knowledge base answer]
```

#### Example 3: Multi-turn Conversation

```
User: Hi!
Bot: Hello! How can I assist you today?

User: How do loops work?
Bot: A loop repeats a block of code... [Detailed explanation]

User: Thanks!
Bot: You're welcome!
```

### Supported Question Types

| Question Type | Example | Response Source |
|---------------|---------|-----------------|
| Python Concept | "What is a function?" | Python Tutor |
| Programming Topic | "Explain machine learning" | Knowledge Base |
| General Greeting | "Hello!" | Intent Classifier |
| Language Question | "Tell me about JavaScript" | Knowledge Base |
| Gratitude | "Thank you!" | Intent Classifier |

---

## Development Guide

### Project Architecture for Developers

#### Adding a New Python Topic

**File:** `src/python_tutor.py`

```python
"your_topic": {
    "level": SkillLevel.BEGINNER,  # or INTERMEDIATE, ADVANCED
    "keywords": ["keyword1", "keyword2"],
    "explanation": {
        "beginner": "Simple explanation...",
        "intermediate": "More detailed...",
        "advanced": "Deep dive..."
    },
    "code": """
# Code example
print("Hello, World!")
""",
    "why_it_works": "Explanation of how the code works",
    "common_mistakes": [
        "Mistake 1",
        "Mistake 2"
    ],
    "best_practices": [
        "Practice 1",
        "Practice 2"
    ]
}
```

#### Adding a New Knowledge Base Topic

**File:** `src/app.py`

```python
KNOWLEDGE_BASE = {
    # ... existing topics
    "your_topic": {
        "keywords": ["keyword1", "keyword2"],
        "answer": "Comprehensive explanation of your_topic..."
    }
}
```

#### Adding a New Intent

**File:** `src/app.py`

```python
TRAINING_DATA = {
    # ... existing intents
    "your_intent": ["phrase1", "phrase2", "phrase3"],
}

RESPONSES = {
    # ... existing responses
    "your_intent": [
        "Response 1",
        "Response 2"
    ]
}
```

#### Retraining the ML Model

The model is automatically trained on startup if not found, or you can retrain it:

```python
# In src/app.py
def train_intent_classifier():
    """Train the intent classifier from TRAINING_DATA"""
    training_texts = []
    training_labels = []
    
    for intent, phrases in TRAINING_DATA.items():
        training_texts.extend(phrases)
        training_labels.extend([intent] * len(phrases))
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    
    pipeline.fit(training_texts, training_labels)
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
```

### Customization Options

#### 1. Change UI Theme

**File:** `templates/index.html`

```css
/* Modify the gradient background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Change button colors */
#input-area button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

#### 2. Modify Response Threshold

**File:** `src/app.py`

```python
# Adjust the knowledge base match threshold
QA_MATCH_THRESHOLD = 0.4  # Lower = more permissive matches
```

#### 3. Add More Training Data

**File:** `src/app.py`

```python
TRAINING_DATA = {
    "greeting": [
        "hello", "hi", "hey",  # existing
        "yo", "sup", "what's good"  # add more
    ]
}
```

### Running Tests

Currently, there are no automated tests. You can add tests using pytest:

```bash
pip install pytest
pytest tests/
```

### Performance Optimization

1. **Model Caching**: ML model is loaded once at startup
2. **Response Caching**: Could implement caching for frequent questions
3. **Lazy Loading**: Knowledge base is loaded once on startup

---

## Features

### Current Features ✅

- **Intent Classification**: ML-powered user intent detection
- **Python Tutoring**: Multi-level Python education
- **Knowledge Base**: Comprehensive programming knowledge
- **Web Interface**: Beautiful, responsive chat UI
- **Code Highlighting**: Syntax highlighting for Python code
- **Markdown Support**: Formatted responses with bold, italic, code
- **Real-time Chat**: Instant message processing

### Potential Future Features 🚀

- **User Authentication**: Save user conversations
- **Conversation History**: Store and retrieve past chats
- **Advanced NLP**: Use more sophisticated NLP models
- **Multi-language Support**: Support languages beyond English
- **Code Execution**: Execute and verify Python code
- **Sentiment Analysis**: Understand user emotions
- **API Integration**: Connect to external APIs (weather, news)
- **Voice Chat**: Voice input and output
- **Mobile App**: Native mobile application
- **Database Integration**: Store user data and preferences

---

## Troubleshooting

### Common Issues & Solutions

#### Issue 1: ModuleNotFoundError

**Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip install -r requirements.txt
# Or install individually
pip install flask scikit-learn numpy textblob
```

#### Issue 2: Port Already in Use

**Problem:**
```
Address already in use: 127.0.0.1:5000
```

**Solution:**
```bash
# Option 1: Use a different port
python src/app.py --port 5001

# Option 2: Kill the process using port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows (find PID, then taskkill)
```

#### Issue 3: Model Not Loading

**Problem:**
```
FileNotFoundError: models/intent_classifier.pkl not found
```

**Solution:**
The model will be automatically trained on first run. If not:
```bash
# Delete the model and let it retrain
rm models/intent_classifier.pkl
python src/app.py
```

#### Issue 4: Slow Response

**Problem:** Responses take too long

**Solutions:**
- Check internet connection
- Increase QA_MATCH_THRESHOLD to reduce search scope
- Add more specific keywords to topics
- Consider caching frequent responses

#### Issue 5: Answers Not Making Sense

**Problem:** Chatbot gives irrelevant responses

**Solutions:**
- Add more training data to intents
- Improve keyword matching
- Adjust TF-IDF parameters
- Retrain the ML model with more examples

### Performance Metrics

| Metric | Value |
|--------|-------|
| Model Load Time | ~100ms |
| Response Generation | ~50-200ms |
| Average Latency | ~300-500ms |
| Memory Usage | ~150-200MB |

### Debugging Tips

1. **Enable Flask Debug Mode:**
```python
app.run(debug=True)
```

2. **Check Intent Classification:**
```python
# Add logging in app.py
print(f"Detected Intent: {predicted_intent}")
print(f"Confidence: {confidence}")
```

3. **Test ML Model:**
```python
# Test model directly
from src.app import pipeline
result = pipeline.predict(["what is a loop"])
print(result)
```

---

## FAQs

**Q: How accurate is the ML model?**
A: The model achieves ~25-32% accuracy on small datasets. For production, train with more data.

**Q: Can I deploy this to production?**
A: Yes! Use Gunicorn or similar WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 src.app:app
```

**Q: How do I save conversations?**
A: Modify `src/app.py` to add database integration (SQLite, MongoDB, etc.)

**Q: Can I use this with Telegram/WhatsApp?**
A: Yes! The Wechaty integration is already in requirements. Configure it for your platform.

**Q: How do I contribute?**
A: Fork the repository, make changes, and submit a pull request.

---

## License

MIT License - Feel free to use for personal and commercial projects.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Last Updated:** May 2026  
**Project Version:** 1.0.0  
**Author:** Pranav Kharat

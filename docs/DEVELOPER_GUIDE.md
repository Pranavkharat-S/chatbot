# Developer Setup & Customization Guide

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Configuration](#project-configuration)
3. [Code Walkthrough](#code-walkthrough)
4. [Extending the Chatbot](#extending-the-chatbot)
5. [Testing & Debugging](#testing--debugging)
6. [Deployment](#deployment)

---

## Development Environment Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
# Navigate to project
cd chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask, sklearn; print('✅ Ready to develop!')"
```

### Option 2: Using Conda

```bash
# Create conda environment
conda create -n chatbot-env python=3.9

# Activate environment
conda activate chatbot-env

# Install dependencies
pip install -r requirements.txt
```

### IDE Setup

**VS Code:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
}
```

**PyCharm:**
1. Open project in PyCharm
2. Go to Settings → Project → Python Interpreter
3. Add Python Interpreter from venv

### Development Tools

```bash
# Install development tools
pip install pytest pytest-cov  # Testing
pip install black flake8       # Code formatting & linting
pip install ipython jupyter    # Interactive development
```

---

## Project Configuration

### Environment Variables

Create `.env` file:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=src/app.py

# Server Configuration
HOST=127.0.0.1
PORT=5000

# Logging
LOG_LEVEL=DEBUG

# ML Model
MODEL_PATH=models/intent_classifier.pkl
QA_THRESHOLD=0.4
```

Load in `src/app.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
MODEL_PATH = os.getenv('MODEL_PATH', 'models/intent_classifier.pkl')
QA_THRESHOLD = float(os.getenv('QA_THRESHOLD', 0.4))
```

### Configuration Files

**config.py** (New file to create):

```python
import os
from pathlib import Path

class Config:
    """Base configuration"""
    FLASK_APP = 'src/app.py'
    MODEL_PATH = Path(__file__).parent / 'models' / 'intent_classifier.pkl'
    QA_THRESHOLD = 0.4
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

---

## Code Walkthrough

### Main Application Flow

```
app.py
├── Load ML Model
├── Initialize Flask App
├── Define Routes
│   ├── GET / → render_template('index.html')
│   └── POST /chat → process_message()
└── Start Server
```

### Processing Pipeline

```python
@app.route('/chat', methods=['POST'])
def chat():
    # 1. Get user message
    data = request.json
    user_message = data.get('message', '').strip()
    
    # 2. Validate input
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # 3. Process message
    response_data = process_message(user_message)
    
    # 4. Return response
    return jsonify(response_data)
```

### Key Functions

**1. Intent Prediction**

```python
def predict_intent(text):
    """Predict user intent using ML model"""
    try:
        predictions = pipeline.predict([text])
        probabilities = pipeline.predict_proba([text])
        confidence = max(probabilities[0])
        return predictions[0], confidence
    except Exception as e:
        return 'default', 0.0
```

**2. Knowledge Base Lookup**

```python
def get_knowledge_response(question):
    """Search knowledge base for matching topic"""
    question_lower = question.lower()
    
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data['keywords']:
            if keyword in question_lower:
                return data['answer'], topic
    
    return None, None
```

**3. Python Tutor Response**

```python
def get_python_tutor_response(question, skill_level='beginner'):
    """Get educational response for Python topic"""
    from python_tutor import get_python_tutor_response as tutor
    return tutor(question, skill_level)
```

### Response Generation

```python
def process_message(user_input):
    """Main message processing pipeline"""
    
    # Step 1: Predict intent
    intent, confidence = predict_intent(user_input)
    
    # Step 2: Try Python tutoring
    python_response = get_python_tutor_response(user_input)
    if python_response:
        return {
            'response': python_response,
            'type': 'python_tutor',
            'metadata': {'topic': 'python', 'skill_level': 'beginner'}
        }
    
    # Step 3: Try knowledge base
    kb_response, topic = get_knowledge_response(user_input)
    if kb_response:
        return {
            'response': kb_response,
            'type': 'knowledge_base',
            'metadata': {'category': topic}
        }
    
    # Step 4: Use intent-based response
    response = random.choice(RESPONSES.get(intent, RESPONSES['default']))
    return {
        'response': response,
        'type': 'intent_response',
        'metadata': {'intent': intent, 'confidence': confidence}
    }
```

---

## Extending the Chatbot

### Adding a New Python Topic

**File:** `src/python_tutor.py`

```python
PYTHON_TOPICS = {
    # ... existing topics ...
    
    "generators": {
        "level": SkillLevel.ADVANCED,
        "keywords": ["generator", "yield", "lazy", "lazy evaluation"],
        "explanation": {
            "beginner": "Generators are functions that return values one at a time, saving memory.",
            "intermediate": "Generators use 'yield' to produce values lazily, pausing execution between yields.",
            "advanced": "Generators implement the iterator protocol with __iter__ and __next__, using couroutines."
        },
        "code": """
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(3):
    print(i)  # Output: 3, 2, 1
""",
        "why_it_works": "Each 'yield' pauses the function and returns a value. Resuming continues from where it paused.",
        "common_mistakes": [
            "Using 'return' instead of 'yield'",
            "Calling generator as a function instead of iterating"
        ],
        "best_practices": [
            "Use generators for large datasets to save memory",
            "Combine with 'for' loops for cleaner code",
            "Use generator expressions for simple cases"
        ]
    }
}
```

### Adding Knowledge Base Topic

**File:** `src/app.py`

```python
KNOWLEDGE_BASE = {
    # ... existing topics ...
    
    "blockchain": {
        "keywords": ["blockchain", "cryptocurrency", "bitcoin", "ethereum"],
        "answer": """Blockchain is a distributed ledger technology that maintains a chain of blocks...
- Decentralized: No single authority controls the chain
- Immutable: Once data is added, it cannot be changed
- Transparent: All transactions are visible to network participants
- Secure: Uses cryptography to protect data

Common applications: Bitcoin, Ethereum, Smart Contracts, Supply Chain"""
    }
}
```

### Adding Intent & Responses

**File:** `src/app.py`

```python
TRAINING_DATA = {
    # ... existing intents ...
    
    "joke": ["tell me a joke", "make me laugh", "something funny", "joke please"],
}

RESPONSES = {
    # ... existing responses ...
    
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
        "How many programmers does it take to change a lightbulb? None, that's a hardware problem! 💡"
    ]
}
```

### Custom Response Processing

Create `src/custom_handlers.py`:

```python
def handle_complex_question(question):
    """Handle complex multi-part questions"""
    # Your custom logic here
    return "Custom response"

def handle_follow_up(current_question, previous_context):
    """Handle follow-up questions with context"""
    # Your custom logic here
    return "Follow-up response"

def extract_entities(question):
    """Extract named entities from question"""
    # Use spaCy or NLTK for NER
    return entities
```

Use in `src/app.py`:

```python
from custom_handlers import handle_complex_question

def process_message(user_input):
    # ... existing logic ...
    
    # Check for complex questions
    if is_complex_question(user_input):
        return {
            'response': handle_complex_question(user_input),
            'type': 'custom_handler'
        }
    
    # ... rest of logic ...
```

---

## Testing & Debugging

### Unit Testing

Create `tests/test_app.py`:

```python
import pytest
from src.app import app, predict_intent, process_message

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chat_endpoint(client):
    """Test /chat endpoint"""
    response = client.post('/chat',
        json={'message': 'Hello'})
    
    assert response.status_code == 200
    assert 'response' in response.json

def test_empty_message(client):
    """Test empty message handling"""
    response = client.post('/chat',
        json={'message': ''})
    
    assert response.status_code == 400

def test_intent_prediction():
    """Test ML intent prediction"""
    intent, confidence = predict_intent("Hello there!")
    
    assert intent == 'greeting'
    assert confidence > 0.5

def test_python_topic_detection():
    """Test Python topic detection"""
    response = process_message("What is a loop?")
    
    assert response['type'] == 'python_tutor'
    assert 'loop' in response['metadata'].get('topic', '').lower()
```

Run tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_app.py::test_chat_endpoint
```

### Debug Mode

Enable debug logging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    logger.debug(f"Received message: {user_message}")
    
    intent, confidence = predict_intent(user_message)
    logger.debug(f"Predicted intent: {intent} (confidence: {confidence})")
    
    # ... rest of function
```

Run with debugging:

```bash
# Flask debug mode
FLASK_ENV=development FLASK_DEBUG=1 python src/app.py

# Python debugger
python -m pdb src/app.py
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_response_generation():
    """Profile response generation performance"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    process_message("What is a decorator?")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions

if __name__ == '__main__':
    profile_response_generation()
```

---

## Deployment

### Deployment with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

### Deployment with Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:app"]
```

Build and run:

```bash
# Build image
docker build -t chatbot:latest .

# Run container
docker run -p 5000:5000 chatbot:latest
```

### Deployment with Heroku

Create `Procfile`:

```
web: gunicorn src.app:app
```

Create `runtime.txt`:

```
python-3.9.16
```

Deploy:

```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Deployment with AWS

1. Use AWS Elastic Beanstalk
2. Configure `.ebextensions/python.config`
3. Deploy with EB CLI

### Environment-Specific Configuration

```python
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    from config import config
    app.config.from_object(config[config_name])
    
    # Load routes
    from routes import register_routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    config_name = os.getenv('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    app.run()
```

---

## Performance Optimization

### Caching Responses

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_knowledge_response(question):
    """Cache frequently asked questions"""
    # ... implementation ...
```

### Database Optimization

```python
# Future: Use Redis for caching
from redis import Redis

redis_client = Redis(host='localhost', port=6379)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Check cache
    cached = redis_client.get(user_message)
    if cached:
        return json.loads(cached)
    
    # Generate response
    response = process_message(user_message)
    
    # Cache response
    redis_client.setex(user_message, 3600, json.dumps(response))
    
    return response
```

### Load Testing

```bash
pip install locust

# Create locustfile.py
# Run: locust -f locustfile.py
```

---

**Happy Developing! 🚀**

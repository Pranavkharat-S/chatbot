# Quick Reference & Cheat Sheet

## Installation Quick Start

```bash
# Clone repository
git clone https://github.com/Pranavkharat-S/chatbot.git
cd chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/app.py

# Open browser
http://localhost:5000
```

---

## Common Commands

### Running the App

```bash
# Development mode
python src/app.py

# With debug mode
FLASK_DEBUG=1 python src/app.py

# With Gunicorn
gunicorn -w 4 src.app:app

# With custom port
python src/app.py --port 5001
```

### Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Package Management

```bash
# Install requirements
pip install -r requirements.txt

# Update single package
pip install --upgrade flask

# Add new package
pip install package-name
pip freeze > requirements.txt

# Uninstall package
pip uninstall package-name
```

### Git Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main
```

---

## API Cheat Sheet

### Send Message

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Python?"}'
```

### Python Requests

```python
import requests

url = "http://localhost:5000/chat"
response = requests.post(url, json={"message": "Hello!"})
print(response.json())
```

### JavaScript Fetch

```javascript
fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: "Hi!"})
})
.then(r => r.json())
.then(d => console.log(d))
```

---

## Project Structure

```
chatbot/
├── src/                    # Source code
│   ├── app.py             # Main Flask app
│   └── python_tutor.py    # Python tutoring
├── models/                # ML models
├── templates/             # Web UI
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
└── README.md             # Main readme
```

---

## File Locations

| What | Location |
|------|----------|
| Main App | `src/app.py` |
| Web UI | `templates/index.html` |
| ML Model | `models/intent_classifier.pkl` |
| Dependencies | `requirements.txt` |
| Python Topics | `src/python_tutor.py` |
| Knowledge Base | `src/app.py` (KNOWLEDGE_BASE dict) |
| Intents | `src/app.py` (TRAINING_DATA dict) |

---

## Key Python Topics Supported

**Beginner:**
- Variables
- Loops
- Functions
- Data types

**Intermediate:**
- List comprehensions
- Decorators
- File handling
- Exception handling

**Advanced:**
- Async/await
- Generators
- Meta-programming
- Memory management

---

## Supported Intents

| Intent | Examples |
|--------|----------|
| greeting | "Hello", "Hi", "Hey" |
| farewell | "Bye", "Goodbye", "See you" |
| help | "Help me", "Assist me" |
| thanks | "Thank you", "Thanks" |
| about | "Who are you?", "What can you do?" |
| weather | "What's the weather?" |
| time | "What time is it?" |

---

## Configuration

### Environment Variables

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Model Configuration

```python
# In src/app.py
MODEL_PATH = Path(__file__).parent / "models" / "intent_classifier.pkl"
QA_MATCH_THRESHOLD = 0.4  # Lower = more permissive
```

---

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src

# Specific test
pytest tests/test_app.py::test_function
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Port in use | Change port or kill process |
| Model not loading | Delete .pkl file, restart app |
| Slow responses | Check network, increase threshold |
| App won't start | Check Python version, check syntax |

---

## Important Functions

| Function | Purpose |
|----------|---------|
| `predict_intent()` | Classify user intent |
| `process_message()` | Main message handler |
| `get_python_tutor_response()` | Python tutoring |
| `get_knowledge_response()` | Knowledge base lookup |

---

## Response Format

```json
{
    "response": "Answer text here...",
    "type": "python_tutor|knowledge_base|intent_response",
    "metadata": {
        "topic": "...",
        "skill_level": "beginner|intermediate|advanced"
    }
}
```

---

## Development Workflow

1. **Setup**: `python -m venv venv && source venv/bin/activate`
2. **Install**: `pip install -r requirements.txt`
3. **Develop**: Edit files in `src/` or `templates/`
4. **Test**: `python src/app.py` → Open browser
5. **Commit**: `git add . && git commit -m "message"`
6. **Push**: `git push origin main`

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Model Load | ~100ms |
| Response Time | ~50-200ms |
| Average Latency | ~300-500ms |
| Memory Usage | ~150-200MB |

---

## Documentation Files

| Document | Purpose |
|----------|---------|
| `COMPLETE_DOCUMENTATION.md` | Full project documentation |
| `API_REFERENCE.md` | API endpoints & examples |
| `DEVELOPER_GUIDE.md` | Development setup & customization |
| `BEGINNER_GUIDE.md` | Beginner-friendly guide |
| `PROJECT_STRUCTURE.md` | Quick structure overview |

---

## Useful Links

- **GitHub**: https://github.com/Pranavkharat-S/chatbot
- **Flask Docs**: https://flask.palletsprojects.com/
- **scikit-learn**: https://scikit-learn.org/
- **Python Docs**: https://docs.python.org/3/

---

## Common Tasks

### Add new Python topic

1. Open `src/python_tutor.py`
2. Add entry to `PYTHON_TOPICS` dict
3. Restart app

### Add new intent

1. Open `src/app.py`
2. Add phrases to `TRAINING_DATA`
3. Add responses to `RESPONSES`
4. Restart app (model retrains)

### Add knowledge topic

1. Open `src/app.py`
2. Add entry to `KNOWLEDGE_BASE` dict
3. Include keywords and answer

### Change UI theme

1. Open `templates/index.html`
2. Modify CSS colors/fonts
3. Refresh browser

### Deploy to production

1. Install Gunicorn: `pip install gunicorn`
2. Run: `gunicorn -w 4 src.app:app`
3. Configure server (Nginx, Apache, etc.)

---

## Debugging Tips

```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log messages
logger.debug(f"Message: {user_input}")
logger.info("Response generated")
logger.error("An error occurred")

# Print debug info
print(f"Intent: {intent}, Confidence: {confidence}")
```

---

**Quick Help**

- 📚 Read Full Docs: `docs/COMPLETE_DOCUMENTATION.md`
- 🔧 Customize: `docs/DEVELOPER_GUIDE.md`
- 🌐 API: `docs/API_REFERENCE.md`
- 🚀 Deploy: `docs/DEVELOPER_GUIDE.md#deployment`

---

**Last Updated:** May 2026

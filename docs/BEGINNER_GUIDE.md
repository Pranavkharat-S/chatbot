# Chatbot Project - Beginner's Guide 📚

Welcome! This guide explains the project structure in simple terms.

---

## 📁 Project Structure

```
chatbot/
│
├── src/                          # 🔧 Source Code (Python files)
│   ├── app.py                    # Main application - runs the chatbot
│   └── python_tutor.py           # AI logic for answering questions
│
├── models/                       # 🤖 Trained ML Model
│   └── intent_classifier.pkl     # AI model file (already trained)
│
├── templates/                    # 🎨 Web Interface
│   └── index.html                # Chat interface (what you see in browser)
│
├── docs/                         # 📖 Documentation
│   └── BEGINNER_GUIDE.md        # This file!
│
├── requirements.txt              # 📦 Dependencies (pip libraries)
├── START_HERE.txt               # Quick start instructions
└── README.md                    # Project overview
```

---

## 🎯 What Does Each Part Do?

### 1. **src/ Folder** (Source Code)
Contains the Python scripts that run the chatbot.

- **app.py**: The main program. This starts the web server.
- **python_tutor.py**: The AI brain. It answers Python questions.

### 2. **models/ Folder** (AI Model)
Contains a pre-trained machine learning model.

- **intent_classifier.pkl**: An AI model that understands what the user is asking about.

### 3. **templates/ Folder** (User Interface)
Contains the web page you see in your browser.

- **index.html**: The chat interface where you type messages and see responses.

### 4. **requirements.txt**
Lists all the Python libraries (packages) you need to install.

---

## 🚀 How to Run (3 Simple Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the App
```bash
python src/app.py
```

### Step 3: Open in Browser
Go to: `http://127.0.0.1:5000`

---

## 💬 What Can You Ask?

Try these questions:

**Python Questions:**
- "What is a variable?"
- "How do loops work?"
- "Explain functions to me"
- "What are decorators?"

**General Questions:**
- "What is machine learning?"
- "Tell me about Python"
- "What is web development?"

**Casual Chat:**
- "Hello!"
- "Thank you"

---

## 📚 Key Files to Know

| File | Purpose | Do I Edit It? |
|------|---------|--------------|
| `src/app.py` | Main application | ✅ Yes, to customize |
| `src/python_tutor.py` | AI logic | ✅ Yes, to add features |
| `templates/index.html` | Web design | ✅ Yes, to change UI |
| `models/intent_classifier.pkl` | AI model | ❌ No, it's pre-trained |
| `requirements.txt` | Dependencies | ✅ Yes, to add packages |

---

## 🔄 How the Chatbot Works (Simple Flow)

```
1. You type a message in the browser
2. Message is sent to app.py
3. python_tutor.py processes the question
4. Intent classifier identifies what you're asking
5. Response is generated and sent back
6. You see the answer in the browser
```

---

## 🆘 Troubleshooting

**Port already in use?**
```bash
python src/app.py --port 5001
```

**Module not found error?**
```bash
pip install -r requirements.txt
```

**App not starting?**
- Check if Python is installed: `python --version`
- Check if you're in the correct folder
- Try running from VS Code terminal

---

## 📖 Next Steps

1. **Run the app** → See it work!
2. **Check `src/app.py`** → Understand the code
3. **Modify `templates/index.html`** → Change the UI
4. **Add your own questions** → Extend functionality
5. **Train a new model** → Customize AI behavior

---

**Happy Learning! 🎉**

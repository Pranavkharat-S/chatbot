# 🚀 QUICK REFERENCE - File Structure Explained

## Project Layout (Super Simple!)

```
chatbot/
├── src/                    👈 Your Python code
│   ├── app.py             👈 START HERE - Run this file
│   └── python_tutor.py    👈 Helper file (AI logic)
│
├── models/                👈 AI brain (don't touch)
├── templates/             👈 Web page design
├── requirements.txt       👈 Libraries to install
└── docs/                  👈 Help files
```

---

## What to Do First

```
1. Install: pip install -r requirements.txt
2. Run:     python src/app.py
3. Visit:   http://127.0.0.1:5000
4. Chat!    Type Python questions
```

---

## File Purposes (1-Sentence Each)

| Folder | File | What It Does |
|--------|------|-------------|
| src/ | **app.py** | Runs the website and chatbot |
| src/ | **python_tutor.py** | Provides AI answers |
| models/ | intent_classifier.pkl | AI model (pre-trained) |
| templates/ | index.html | The chat website you see |
| — | requirements.txt | Python packages to install |
| docs/ | BEGINNER_GUIDE.md | Full guide (this you're reading) |

---

## Common Edits

**Want to change the design?**
→ Edit `templates/index.html`

**Want to change responses?**
→ Edit `src/python_tutor.py`

**Want to add a new library?**
→ Edit `requirements.txt` and run `pip install -r requirements.txt`

---

That's it! You now understand the project structure. 😊

# API Reference Guide

## Overview

The Chatbot API provides a single endpoint for sending messages and receiving intelligent responses.

---

## REST API Endpoints

### 1. Get Home Page

**Endpoint:** `/`  
**Method:** GET

**Description:** Serves the chat interface HTML

**Response:**
- **Status:** 200 OK
- **Content-Type:** text/html
- **Body:** index.html content

**Example:**
```bash
curl http://localhost:5000/
```

---

### 2. Send Chat Message

**Endpoint:** `/chat`  
**Method:** POST

**Description:** Sends a message and gets an intelligent response

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "message": "What is a list comprehension?"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | User message or question |

**Response Body (Success - 200):**
```json
{
    "response": "A list comprehension is a concise and efficient way to create lists in Python...",
    "type": "python_tutor",
    "metadata": {
        "topic": "list comprehensions",
        "skill_level": "intermediate",
        "includes_code": true
    }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| response | string | The chatbot's response |
| type | string | Response type (python_tutor, knowledge_base, intent_response) |
| metadata | object | Additional information about the response |

**Metadata Fields (varies by type):**

For `python_tutor` responses:
```json
{
    "topic": "string - the Python topic",
    "skill_level": "string - beginner/intermediate/advanced",
    "includes_code": "boolean - whether code examples included"
}
```

For `knowledge_base` responses:
```json
{
    "category": "string - topic category",
    "keywords_matched": "array - matched keywords"
}
```

For `intent_response` responses:
```json
{
    "intent": "string - detected intent",
    "confidence": "number - confidence score"
}
```

**Response Body (Error - 400):**
```json
{
    "error": "Message cannot be empty"
}
```

**HTTP Status Codes:**

| Status | Meaning |
|--------|---------|
| 200 | Success - response returned |
| 400 | Bad Request - invalid input |
| 405 | Method Not Allowed - wrong HTTP method |
| 500 | Internal Server Error |

---

## Request Examples

### Example 1: Python Tutoring Request

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do decorators work?"}'
```

**Response:**
```json
{
    "response": "Decorators are functions that modify or enhance other functions or methods without permanently changing their source code...",
    "type": "python_tutor",
    "metadata": {
        "topic": "decorators",
        "skill_level": "advanced",
        "includes_code": true
    }
}
```

### Example 2: Knowledge Base Request

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

**Response:**
```json
{
    "response": "Machine Learning is a subset of Artificial Intelligence...",
    "type": "knowledge_base",
    "metadata": {
        "category": "Machine Learning",
        "keywords_matched": ["machine learning", "artificial intelligence"]
    }
}
```

### Example 3: Intent Classification Request

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello there!"}'
```

**Response:**
```json
{
    "response": "Hi there! What can I do for you?",
    "type": "intent_response",
    "metadata": {
        "intent": "greeting",
        "confidence": 0.95
    }
}
```

### Example 4: JavaScript Request

```bash
fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "What is a variable?"
  })
})
.then(response => response.json())
.then(data => console.log(data.response))
.catch(error => console.error('Error:', error));
```

### Example 5: Python Request

```python
import requests
import json

url = "http://localhost:5000/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "How do loops work?"}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print(result['response'])
print(f"Type: {result['type']}")
print(f"Metadata: {result['metadata']}")
```

---

## Response Types

### 1. Python Tutor Response

**When:** User asks about Python concepts

**Example Topics:**
- "What is a variable?"
- "How do decorators work?"
- "Explain async/await"
- "What is list comprehension?"

**Response Structure:**
```json
{
    "response": "Detailed explanation with code examples...",
    "type": "python_tutor",
    "metadata": {
        "topic": "string",
        "skill_level": "beginner|intermediate|advanced",
        "includes_code": true
    }
}
```

### 2. Knowledge Base Response

**When:** User asks about general programming topics

**Example Topics:**
- "What is machine learning?"
- "Tell me about web development"
- "What is JavaScript?"
- "Explain data science"

**Response Structure:**
```json
{
    "response": "Topic explanation from knowledge base...",
    "type": "knowledge_base",
    "metadata": {
        "category": "string",
        "keywords_matched": ["keyword1", "keyword2"]
    }
}
```

### 3. Intent Response

**When:** User sends a greeting, farewell, or intent-based message

**Intent Types:**
- `greeting`: "Hello", "Hi", "Hey"
- `farewell`: "Bye", "Goodbye", "See you"
- `help`: "Help me", "Assist me", "Teach me"
- `thanks`: "Thank you", "Thanks", "Appreciate"
- `about`: "Who are you?", "What can you do?"
- `weather`: "What's the weather?"
- `time`: "What time is it?"

**Response Structure:**
```json
{
    "response": "Intent-based response...",
    "type": "intent_response",
    "metadata": {
        "intent": "string",
        "confidence": 0.0-1.0
    }
}
```

---

## Error Handling

### Error Codes & Messages

**400 - Bad Request**
```json
{
    "error": "Message cannot be empty"
}
```

**400 - Invalid JSON**
```json
{
    "error": "Invalid JSON in request body"
}
```

**500 - Server Error**
```json
{
    "error": "Internal server error occurred"
}
```

### Error Handling in Code

**JavaScript:**
```javascript
fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({message: "Hello"})
})
.then(r => {
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
})
.catch(e => console.error('Error:', e));
```

**Python:**
```python
try:
    response = requests.post('/chat', json={'message': 'Hello'})
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

---

## Rate Limiting & Performance

### Current Limits

| Metric | Value |
|--------|-------|
| Request Timeout | 30 seconds |
| Max Message Length | 1000 characters |
| Response Latency | 50-500ms |
| Concurrent Requests | Unlimited (Flask default) |

### Performance Tips

1. **Batch Requests:** Group multiple messages
2. **Cache Responses:** Store frequent questions
3. **Use CDN:** Cache static files (CSS, JS)
4. **Optimize Queries:** Minimize knowledge base lookups

---

## Integration Examples

### Integrate with Telegram

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    response = requests.post('http://localhost:5000/chat',
        json={'message': user_message})
    bot_response = response.json()['response']
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_response
    )

# Setup and run
app = Application.builder().token('YOUR_TOKEN').build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
```

### Integrate with Discord

```python
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    response = requests.post('http://localhost:5000/chat',
        json={'message': message.content})
    bot_response = response.json()['response']
    
    await message.channel.send(bot_response)

bot.run('YOUR_TOKEN')
```

### Integrate with Slack

```python
from slack_bolt import App
import requests

app = App(token="xoxb-YOUR-TOKEN", signing_secret="YOUR-SECRET")

@app.message("")
def handle_message(message, say):
    response = requests.post('http://localhost:5000/chat',
        json={'message': message['text']})
    bot_response = response.json()['response']
    say(bot_response)

app.start(port=int(os.environ.get("PORT", 3000)))
```

---

## Versioning

**Current API Version:** 1.0.0

Future versions may include:
- Request/response formats
- New endpoints
- Authentication
- Rate limiting

---

## Support

For API issues:
1. Check error messages
2. Verify request format
3. Check server logs
4. Review this documentation
5. Open GitHub issue

---

**Last Updated:** May 2026

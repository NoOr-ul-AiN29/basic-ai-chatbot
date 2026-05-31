# 🤖 Basic AI Chatbot

A beginner-friendly, production-style AI chatbot built with **Python**, **Streamlit**, and the **OpenAI API**. Features a modern dark UI, persistent chat history, and clean modular code — perfect for an internship project or portfolio piece.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🧠 AI-powered | Uses OpenAI GPT-3.5-turbo (upgradeable to GPT-4o) |
| 💬 Chat history | Full conversation context sent with every request |
| 🎨 Modern dark UI | Custom CSS with animated message bubbles |
| ⚡ Typing indicator | Animated dots while the AI is thinking |
| 🛡️ Error handling | Friendly messages for auth, quota, and network errors |
| 🧩 Modular code | Separated into `app.py`, `chatbot.py`, `utils/` |
| 🔒 Secure | API key stored in `.env`, never in source code |

---

## 🗂️ Project Structure

```
basic-ai-chatbot/
│
├── app.py              ← Streamlit frontend (UI + session state)
├── chatbot.py          ← OpenAI API wrapper (get_ai_response)
├── requirements.txt    ← Python dependencies
├── .env                ← Your API key (NOT committed to Git)
├── .gitignore          ← Excludes .env, venv, __pycache__
├── README.md           ← This file
│
├── utils/
│   ├── __init__.py     ← Makes utils a Python package
│   └── error_handler.py← Converts API exceptions to friendly messages
│
└── assets/
    └── style.css       ← Custom dark UI styles injected into Streamlit
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- An OpenAI account and API key (free tier works)

---

### Step 1 — Clone or download the project

```bash
git clone https://github.com/your-username/basic-ai-chatbot.git
cd basic-ai-chatbot
```

Or simply download and unzip the folder.

---

### Step 2 — Create a virtual environment

A virtual environment keeps this project's dependencies isolated from your system Python.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal — that means it's active.

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs Streamlit, the OpenAI SDK, and python-dotenv.

---

### Step 4 — Get your OpenAI API key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in (or create a free account)
3. Click **"Create new secret key"**
4. Copy the key (it starts with `sk-...`)

> ⚠️ **Important:** You only see the key once. Copy it immediately.

---

### Step 5 — Configure your API key

Open the `.env` file in the project root and replace the placeholder:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 🔒 The `.env` file is listed in `.gitignore` so it will never be accidentally committed to Git.

---

### Step 6 — Run the app

```bash
streamlit run app.py
```

Streamlit will open the app automatically at [http://localhost:8501](http://localhost:8501).

---

## 🧠 How the System Works

### Architecture overview

```
┌─────────────────────────────────────────┐
│              Browser (User)             │
│         http://localhost:8501           │
└──────────────────┬──────────────────────┘
                   │  HTTP (Streamlit)
┌──────────────────▼──────────────────────┐
│               app.py                    │
│  • Renders UI (chat bubbles, input)     │
│  • Manages st.session_state.messages    │
│  • Calls get_ai_response() on submit    │
└──────────────────┬──────────────────────┘
                   │  Python function call
┌──────────────────▼──────────────────────┐
│             chatbot.py                  │
│  • Loads OPENAI_API_KEY from .env       │
│  • Sends messages list to OpenAI API    │
│  • Returns the AI reply string          │
└──────────────────┬──────────────────────┘
                   │  HTTPS (REST API)
┌──────────────────▼──────────────────────┐
│         OpenAI API (cloud)              │
│   POST /v1/chat/completions             │
│   Model: gpt-3.5-turbo                 │
└─────────────────────────────────────────┘
```

### How the frontend connects with the backend

`app.py` is both frontend and backend in a Streamlit app — Streamlit runs your Python script as a server and serves the resulting HTML/JS to the browser. When the user submits a message:

1. Streamlit re-runs the entire `app.py` script from top to bottom.
2. The new user message is appended to `st.session_state.messages`.
3. `get_ai_response()` (from `chatbot.py`) is called with the full message history.
4. The OpenAI SDK sends an HTTPS POST request to `https://api.openai.com/v1/chat/completions`.
5. The AI reply is appended to `st.session_state.messages` and the page re-renders.

### How Streamlit session state works

Normally, every time a user interacts with a Streamlit app, the Python script re-runs completely — all local variables are reset. `st.session_state` is a special persistent dictionary that **survives re-runs** within the same browser session. We use it to store the chat history so messages aren't lost on every interaction.

```python
# Initialise (runs once per session)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Append a message
st.session_state.messages.append({"role": "user", "content": "Hello!"})

# Read messages (persists across re-runs)
for msg in st.session_state.messages:
    print(msg)
```

### How API requests are sent

`chatbot.py` uses the official OpenAI Python SDK (v1.x). The key call is:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",    "content": "You are a helpful assistant."},
        {"role": "user",      "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language..."},
        {"role": "user",      "content": "Give me an example."},
    ],
    temperature=0.7,
    max_tokens=1024,
)
```

Sending the full history with every request is what allows the model to maintain context across turns.

---

## ☁️ Deploy on Streamlit Cloud (Free)

Streamlit Community Cloud lets you deploy this app publicly for free in minutes.

### Steps

1. **Push your code to GitHub**
   - Make sure `.env` is in `.gitignore` (it already is).
   - Do NOT push your `.env` file.

2. **Go to** [https://streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub.

3. **Click "New app"** → select your repo, branch, and set **Main file path** to `app.py`.

4. **Add your secret:**
   - In the deployment settings, go to **"Advanced settings" → "Secrets"**.
   - Add your API key in TOML format:
     ```toml
     OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
     ```
   - This replaces the `.env` file in the cloud environment.

5. **Click "Deploy!"** — your app will be live at a public URL in ~60 seconds.

> Streamlit secrets are stored securely and injected as environment variables, so `os.getenv("OPENAI_API_KEY")` works identically to your local `.env`.

---

## 📸 Screenshots

> _Add screenshots here after running the app._
>
> Suggested shots:
> - Empty state (fresh chat)
> - Active conversation
> - Error message (wrong API key)

---

## 🔧 Customisation

| What to change | Where |
|---|---|
| AI personality / behaviour | `SYSTEM_PROMPT` in `chatbot.py` |
| GPT model (e.g. gpt-4o) | `model=` in `chatbot.py` |
| Creativity level | `temperature=` in `chatbot.py` |
| UI colours & fonts | `assets/style.css` |
| Sidebar content | `with st.sidebar:` block in `app.py` |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥ 1.35 | Web app framework |
| `openai` | ≥ 1.30 | OpenAI Python SDK |
| `python-dotenv` | ≥ 1.0 | Load `.env` variables |

---

## 📄 License

MIT — free to use, modify, and distribute.
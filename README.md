# 🧠 AI BlogBoost — LangChain-Powered Blog Automation for DEV.to

> ✨ Auto-generate, format, and publish blog posts to [DEV.to](https://dev.to) using LangChain + Playwright.

---

## 📽️ Demo
https://github.com/k7kaushal/BlogBoost/blob/main/DEMO.mp4

---

## Features

- ✅ **LangChain  Workflow**
- ✍️ Auto-generates Markdown blog posts
- 🔑 Secure login to DEV.to via Playwright
- 🛠️ Fully async architecture with retry-friendly nodes
- 💡 Modular pipeline: generate → format → publish
- 📦 Easily extendable to Medium, Hashnode, or other platforms

---

## 📦 Setup

### 1. Clone the Repository

```bash
git clone https://gitlab.com/k7kaushal/BlogBoost/.git
```

### 2. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # Or `.venv\Scripts\activate` on Windows

pip install -r requirements.txt
```

> Required: Python 3.10+

### 3. Setup Environment Variables

Create a `.env` file:

```ini
DEVTO_EMAIL=your_email@example.com
DEVTO_PASSWORD=your_password
HF_API_TOKEN=huggingface_token
```

---

## ⚙️ Running the Pipeline

```bash
python LangChain_workflow/main.py
```

This will:
- Generate a blog post using an LLM
- Use Playwright to log in to DEV.to
- Automatically publish the post with selected tags

---

## Note

- Your credentials are read from `.env` file (never hardcoded).
- Make sure `.env` is listed in `.gitignore`.

---


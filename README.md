# Smart Web Research Agent — Setup Guide

## 📁 Project Structure

```
smart_research_agent/
│
├── frontend/
│   └── smart_research_agent.html   ← Open this in browser
│
├── backend/
│   ├── app.py           ← Main server (run this)
│   ├── agent.py         ← Core agent pipeline
│   ├── search.py        ← DuckDuckGo search
│   ├── scraper.py       ← Web scraping
│   ├── summarizer.py    ← AI summarization
│   └── requirements.txt ← Python libraries
│
└── README.md
```

---

## ⚙️ SETUP STEPS

### Step 1 — Install Python
Make sure Python 3.9 or higher is installed.
Download from: https://python.org

### Step 2 — Open Terminal in backend folder
In VS Code: right click backend folder → Open in Terminal

### Step 3 — Install all libraries
```
pip install -r requirements.txt
```

### Step 4 — Set your API Key
In the terminal run:

Windows:
```
set ANTHROPIC_API_KEY=your_api_key_here
```

Mac/Linux:
```
export ANTHROPIC_API_KEY=your_api_key_here
```

Get your free API key from: https://console.anthropic.com

### Step 5 — Start the backend server
```
python app.py
```

You will see:
```
Running at: http://localhost:5000
```

### Step 6 — Open the frontend
Open smart_research_agent.html using VS Code Live Server.

---

## ✅ How It Works

1. User types query in frontend
2. Frontend sends query to backend at http://localhost:5000/research
3. Backend searches web → scrapes pages → processes content → summarizes with AI
4. Backend returns structured result to frontend
5. Frontend displays Summary, Key Points, and Sources

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| Failed to fetch | Make sure backend is running (python app.py) |
| ModuleNotFoundError | Run pip install -r requirements.txt |
| API key error | Set ANTHROPIC_API_KEY in terminal |
| No results found | Try a different search query |



@"
---
title: Smart Research Agent
emoji: 🔍
colorFrom: blue
colorTo: cyan
sdk: docker
pinned: false
---

# Smart Web Research AI Agent
An AI-powered research assistant using Groq LLaMA 3.3
"@ | Out-File -FilePath "README.md" -Encoding utf8
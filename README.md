# 🧠 Multi-Agent AI Research System

An end-to-end AI research assistant that performs web search, content extraction, report generation, and critique using a local LLM (TinyLlama) and LangChain.

---

## 🚀 Features

- 🔍 Web Search using Tavily API
- 🌐 Web Scraping using BeautifulSoup
- ✍️ AI Report Generation (TinyLlama)
- 🧠 AI Critique System
- 💻 Streamlit UI for interaction
- 🔗 Modular pipeline design

---

## 🏗️ Architecture

User Input → Search Tool → Scraper → LLM → Report → Critic

---

## ⚙️ Tech Stack

- Python
- LangChain
- HuggingFace Transformers
- TinyLlama (Local LLM)
- Tavily API
- Streamlit
- BeautifulSoup

---

## 📂 Project Structure

multi_agent_system/
│
├── app.py # Streamlit UI
├── agents.py # Pipeline logic
├── tools.py # Search + Scraping tools
├── llm.py # LLM setup
├── requirements.txt
└── .gitignore


---

## 🧪 How to Run

### 1. Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/multi_agent_system.git
cd multi_agent_system
2. Create virtual environment
uv venv
.venv\Scripts\activate
3. Install dependencies
uv pip install -r requirements.txt
4. Add API key

Create .env file:

TAVILY_API_KEY=your_api_key
5. Run app
uv run streamlit run app.py

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",   # ← updated
        temperature=0.5,
        max_tokens=700,
    )
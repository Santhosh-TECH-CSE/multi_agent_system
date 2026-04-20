from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
from rich import print, text

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web and return relevant results including titles and URLs."""
    response = tavily_client.search(query=query, max_results=5)

    clean_results = []

    for r in response.get("results", []):
        title = r.get("title", "")
        url = r.get("url", "")

        clean_results.append(f"{title} | {url}")

    return "\n".join(clean_results)


# print(web_search.invoke("What is the latest news on AI?"))


@tool
def scrape_url(url: str) -> str:
    """Extract readable text content from a given webpage URL."""

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        # 🚫 REMOVE garbage
        if any(x in text.lower() for x in ["access denied", "cloudflare", "enable cookies"]):
            return ""

        return text[:1500]

    except:
        return ""
    
# print(scrape_url.invoke("https://www.cricbuzz.com"))
import os
from langchain_ollama import ChatOllama
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from langgraph.prebuilt import create_react_agent
from utils import load_system_prompt

@tool
def scrape_job_url(url: str):
  """
  Fetches a URL and returns cleaned text suitable for LLM consumption.

  Args:
    url: The full URL of the job posting or page to fetch.
  """
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.9",
  }
  try:
    response = requests.get(url, headers=headers, timeout=8)
    response.raise_for_status()  # Raise an exception for bad status codes
    html = response.text
  except requests.exceptions.RequestException as e:
    return f"Error fetching url: {e}"
  
  try:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string if soup.title and soup.title.string else "").strip()
    main = soup
    for tag in main(["script", "style", "noscript", "iframe"]):
      tag.decompose()

    text = main.get_text(separator="\n", strip=True)
    # collapse and clean lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cleaned = "\n".join(lines)

    if len(cleaned) > 4000:
        cleaned = cleaned[: 4000 - 1] + "\n\n[TRUNCATED]"

    return f"URL: {url}\nTitle: {title}\n\n{cleaned}"
  except Exception as e:
    return f"ERROR: parsing HTML: {e}"

model = ChatOllama(model="llama3.1:8b")
print(load_system_prompt("summarizer.md"))

agent = create_react_agent(
  model=model,
  tools=[scrape_job_url],
  prompt=load_system_prompt("summarizer.md")
)

print(model.invoke("What is agentic AI?"))
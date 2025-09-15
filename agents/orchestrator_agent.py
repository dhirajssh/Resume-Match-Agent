from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from utils import load_system_prompt

model = ChatOllama(model = "llama3.1:8b")

orchestrator_agent = create_react_agent(
  model=model,
  prompt=load_system_prompt("orchestrator.md")
)
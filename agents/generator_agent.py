import os
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from utils import load_system_prompt
import streamlit as st

model = ChatOllama(model="llama3.1:8b")
prompt = load_system_prompt("generator.md")

resume_path = os.path.join(os.path.dirname(__file__), "..", "resume.md")
if os.path.exists(resume_path):
  resume = load_system_prompt("resume.md")
  st.session_state.resume = resume
else:
  resume = st.session_state.resume

full_prompt = f"{prompt}\n\n---\n\n{resume}"

generator_agent = create_react_agent(
  model=model,
  prompt=full_prompt
)
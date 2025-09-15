from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from utils import load_system_prompt
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class OrchestratorResponse(BaseModel):
  """Structured response for the orchestrator agent."""
  agent:str = Field(
    ...,
    description="""
    Specifies which agent should handle the request.

    - "summarizer_agent": Use when the user provides a job URL and the job description needs to be fetched and summarized.
    - "generator_agent": Use when no URL is provided. This applies to cover letter requests, answering application questions, or any other scenario without a job link.
    """,
    examples=[
      "summarizer_agent",
      "generator_agent",
    ]
  )
  link: Optional[str] = Field(
    default=None,
    description="""
      The job application URL provided by the user.
      This is required when `agent` is "summarizer_agent".
      If no URL is provided by the user, this should remain None.
    """,
    examples=[
      "https://boards.greenhouse.io/company/jobs/1234567",
    ]
  )
  message: Optional[str] = Field(
    default=None,
    description="""
      The original user message.
      Required when `agent` is "generator_agent".
      Otherwise, can be None.
    """,
    examples=[
      "I need a cover letter for the software engineer position.",
      "Why am I a good fit for this role?",
    ]
  )

  @field_validator('agent')
  @classmethod
  def check_agent(cls, value:str)->str:
    field_info = cls.model_fields["agent"]
    description = field_info.description
    examples = set(field_info.examples)

    if value not in examples:
      raise ValueError(
        f"The value of this field should be one of 2: {examples}."
        f"\n\nWas provided invalid value: {value}"
        f"\n\nField Description: {description}"
      )
    return value

def initialize_orchestrator_agent():
  model = ChatOllama(model = "llama3.1:8b")

  orchestrator_agent = create_react_agent(
    model=model,
    prompt=load_system_prompt("orchestrator.md"),
    response_format=OrchestratorResponse
  )
  return orchestrator_agent
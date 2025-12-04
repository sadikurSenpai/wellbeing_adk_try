from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from .utils import load_chat_instruction
from dotenv import load_dotenv
load_dotenv()

llm = LiteLlm(model='openai/gpt-4o')

def get_agent(user_id: str) -> Agent:
    return Agent(
        name = 'chatting_agent',
        model = llm,
        description = "You are a helpful agent who act like a well-being therapist who cares about people's mental health and well-being.",
        instruction = load_chat_instruction(user_id)
    )
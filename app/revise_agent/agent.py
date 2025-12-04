from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from .utils import load_chat_instruction
from dotenv import load_dotenv
load_dotenv()
# dummy user data 
dummy_user_id = 'demo_Alice_b3fe'

llm = LiteLlm(model='openai/gpt-4o')

root_agent = Agent(
    name = 'revise_agent',
    model = llm,
    description = "You are a helpful agent who act like a well-being therapist who cares about people's mental health and well-being.",
    instruction = load_chat_instruction(dummy_user_id)
)
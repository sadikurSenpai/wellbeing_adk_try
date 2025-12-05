import os
import sys
from jinja2 import Template
# Add the parent directory (app) to sys.path to allow importing 'service'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.service.retriever.retrieval_service import retrieve_user_data

_template_cache = None


async def load_chat_instruction(user_id: str, message: str, session_id: str = None):
    global _template_cache
    
    if _template_cache is None:
        # Prompts are now in the parent directory's 'prompts' folder
        prompt_path = os.path.join(parent_dir, 'prompts', 'chat_instruction.j2')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            _template_cache = Template(f.read())

    # Always retrieve fresh context based on the specific message
    # We cannot cache this per session because what is "relevant" changes with every question.
    retrieved_data = await retrieve_user_data(user_id, message)
    
    journals = "\n".join([f"- {doc.page_content}" for doc in retrieved_data['journals']])
    affirmations = "\n".join([f"- {doc.page_content}" for doc in retrieved_data['affirmations']])
    past_chat_history = "\n".join([f"- {doc.page_content}" for doc in retrieved_data['chat_history']])
    user_profile = retrieved_data.get('user_profile')

    if not user_profile:
        user_profile = {
            "name": "Unknown",
            "age": "Unknown",
            "sex": "Unknown",
        }
        
    return _template_cache.render(
        user_profile=user_profile,
        journals=journals if journals else "No recent journals found.",
        affirmations=affirmations if affirmations else "No affirmations found.",
        past_chat_history=past_chat_history if past_chat_history else "No relevant past conversations found."
    )







import os
import sys
from jinja2 import Template
# Add the parent directory (app) to sys.path to allow importing 'service'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from service.retrieval.retrieve_user_data import get_user_data

_template_cache = None

def load_chat_instruction(user_id: str):
    global _template_cache
    if _template_cache is None:
        # Prompts are now in the parent directory's 'prompts' folder
        prompt_path = os.path.join(parent_dir, 'prompts', 'chat_instruction.j2')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            _template_cache = Template(f.read())

    user_profile = get_user_data(user_id)
    
    if not user_profile:
        user_profile = {
            "name": "Unknown",
            "age": "Unknown",
            "sex": "Unknown",
        }
        
    return _template_cache.render(user_profile=user_profile)







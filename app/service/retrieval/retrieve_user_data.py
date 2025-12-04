import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "dummy_data", "user.json")

def get_user_data(user_id: str):
    """
    Retrieves user profile from the JSON 'database'.
    """
    if not os.path.exists(DATA_FILE):
        return None
    
    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        content = f.read()
        data = json.loads(content)
        return data.get(user_id)
import json
import os
import aiofiles

DATA_FILE = "app/data/users.json"

async def get_user_profile(user_id: str):
    """
    Retrieves user profile from the JSON 'database'.
    """
    if not os.path.exists(DATA_FILE):
        return None
    
    async with aiofiles.open(DATA_FILE, mode='r') as f:
        content = await f.read()
        data = json.loads(content)
        return data.get(user_id)
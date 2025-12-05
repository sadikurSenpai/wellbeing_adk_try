import asyncio
from typing import AsyncGenerator, Optional
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from app.chatting_agent.agent import get_agent

# Global session service (in-memory)
# We instantiate it once so it persists across requests in memory
session_service = InMemorySessionService()
APP_NAME = "chatting_agent"

async def get_or_create_session(user_id: str, session_id: Optional[str] = None) -> str:
    """
    Retrieves an existing session ID or creates a new one.
    """
    if session_id:
        return session_id
    
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
    )
    return new_session.id

async def generate_chat_stream(user_id: str, message: str, session_id: str) -> AsyncGenerator[str, None]:
    """
    Generates a stream of responses from the agent for the given session.
    """
    runner = Runner(
        agent=await get_agent(user_id, message, session_id), 
        app_name=APP_NAME, 
        session_service=session_service
    )

    user_msg = Content(role="user", parts=[Part(text=message)])

    try:
        # Attempt to pass stream=True to run_async
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_msg, stream=True):
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            yield part.text
                            await asyncio.sleep(0)
                elif isinstance(event.content, str):
                    yield event.content
                    await asyncio.sleep(0)
    except TypeError:
        # Fallback if stream=True is not accepted by run_async
        print("DEBUG: run_async does not accept stream=True, falling back")
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_msg):
             if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            yield part.text
                            await asyncio.sleep(0)
                elif isinstance(event.content, str):
                    yield event.content
                    await asyncio.sleep(0)
    except Exception as e:
        print(f"DEBUG: Error in stream: {e}")
        yield f"\n[Error: {str(e)}]"
import asyncio
from typing import AsyncGenerator, Optional
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from app.revise_agent.agent import get_agent

# Global session service (in-memory)
# We instantiate it once so it persists across requests in memory
session_service = InMemorySessionService()
APP_NAME = "revise_agent"

async def get_or_create_session(user_id: str, session_id: Optional[str] = None) -> str:
    """
    Retrieves an existing session ID or creates a new one.
    """
    if session_id:
        # In a real DB-backed service, we might verify existence here.
        # For InMemory, we assume the client provided a valid ID from a previous response.
        # If it's invalid, the runner might error out, which we can handle.
        return session_id
    
    # Create new session
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
        agent=get_agent(user_id), 
        app_name=APP_NAME, 
        session_service=session_service
    )

    user_msg = Content(role="user", parts=[Part(text=message)])

    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_msg):
            # Handle streaming content (deltas)
            if hasattr(event, 'content') and event.content:
                # Check for parts with text in the content
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            yield part.text
                # Fallback for simple string content
                elif isinstance(event.content, str):
                    yield event.content
    except Exception as e:
        # In a stream, we can't raise HTTP exception easily once started, 
        # so we might yield an error message or log it.
        # For now, let's yield a generic error message so the user sees something went wrong.
        yield f"\n[Error: {str(e)}]"
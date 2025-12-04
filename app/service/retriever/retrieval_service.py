from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

import asyncio
import time

# Initialize Global Instances (Singleton Pattern)
# This prevents re-initializing connections on every request, significantly reducing latency.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
index_name = os.getenv("PINECONE_INDEX_NAME")

journal_vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="thought")
affirmation_vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="affirmation")
chat_vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="chat_history")
tool_usage_vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="mood")

from app.service.user_profile.user_service import get_user_profile

async def retrieve_user_data(user_id: str, query: str, k: int = 5):
    """
    Retrieves top k journals and affirmations for a specific user based on a query.
    Also retrieves user profile from the JSON database.
    """
    
    # Define Filters
    journal_filter = {"user_id": {"$eq": user_id}, "type": {"$eq": "journal"}}
    affirmation_filter = {"user_id": {"$eq": user_id}, "type": {"$eq": "affirmation"}}
    chat_filter = {"user_id": {"$eq": user_id}, "type": {"$eq": "chat_history"}}
    
    # Execute Async Parallel Search
    # Note: PineconeVectorStore.asimilarity_search is the async method
    t_start = time.time()
    results = await asyncio.gather(
        journal_vectorstore.asimilarity_search(query, k=k, filter=journal_filter),
        affirmation_vectorstore.asimilarity_search(query, k=k, filter=affirmation_filter),
        chat_vectorstore.asimilarity_search(query, k=k, filter=chat_filter),
        get_user_profile(user_id)
    )
    t_end = time.time()
    print(f"DEBUG: Retrieval Time (Parallel): {t_end - t_start:.4f}s")
    
    return {
        "journals": results[0],
        "affirmations": results[1],
        "chat_history": results[2],
        "user_profile": results[3]
    }

async def retrieve_tool_usage_history(user_id: str, mood: str, k: int = 5):
    """
    Retrieves past tool usage history for a specific user based on their mood.
    """
    filter_dict = {"user_id": {"$eq": user_id}, "type": {"$eq": "tool_usage"}}
    
    # Search for past instances where the mood was similar
    results = await tool_usage_vectorstore.asimilarity_search(mood, k=k, filter=filter_dict)
    return results

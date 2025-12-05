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
    t_start = time.time()
    
    # 1. Generate Embedding ONCE (Optimization)
    query_vector = await embeddings.aembed_query(query)
    
    # 2. Search by Vector (Parallel using Threads)
    # We use run_in_executor to ensure true parallelism if the async implementation blocks
    loop = asyncio.get_running_loop()
    
    # Helper for timing
    async def timed_search(name, func):
        t0 = time.time()
        res = await loop.run_in_executor(None, func)
        t1 = time.time()
        return res, t1 - t0

    try:
        # Execute in parallel with timing
        results = await asyncio.wait_for(
            asyncio.gather(
                timed_search("journal", lambda: journal_vectorstore.similarity_search_by_vector(query_vector, k=3, filter=journal_filter)),
                timed_search("affirmation", lambda: affirmation_vectorstore.similarity_search_by_vector(query_vector, k=3, filter=affirmation_filter)),
                timed_search("chat_history", lambda: chat_vectorstore.similarity_search_by_vector(query_vector, k=3, filter=chat_filter)),
                get_user_profile(user_id) # Profile is already async, usually fast
            ),
            timeout=3.0
        )
        
        # Unpack results
        journals, t_journal = results[0]
        affirmations, t_affirmation = results[1]
        chat_history, t_chat = results[2]
        user_profile = results[3]
        
        # Profile timing (approximate since it ran in gather)
        t_profile = 0.0 
        
    except asyncio.TimeoutError:
        print("DEBUG: Retrieval Timed Out (3.0s limit)")
        journals, affirmations, chat_history, user_profile = [], [], [], None
        t_journal = t_affirmation = t_chat = t_profile = 3.0

    t_end = time.time()
    total_retrieval_time = t_end - t_start
    
    metrics = {
        "total_retrieval": total_retrieval_time,
        "journal": t_journal,
        "affirmation": t_affirmation,
        "chat_history": t_chat,
        "profile": t_profile,
        "journal_count": len(journals),
        "affirmation_count": len(affirmations),
        "chat_count": len(chat_history)
    }
    
    print(f"DEBUG: Retrieved {len(journals)} journals, {len(affirmations)} affirmations")
    
    return {
        "journals": journals,
        "affirmations": affirmations,
        "chat_history": chat_history,
        "user_profile": user_profile,
        "metrics": metrics
    }

async def retrieve_tool_usage_history(user_id: str, mood: str, k: int = 5):
    """
    Retrieves past tool usage history for a specific user based on a query.
    """
    filter_dict = {"user_id": {"$eq": user_id}, "type": {"$eq": "tool_usage"}}
    
    # Search for past instances where the mood was similar
    results = await tool_usage_vectorstore.asimilarity_search(mood, k=k, filter=filter_dict)
    return results

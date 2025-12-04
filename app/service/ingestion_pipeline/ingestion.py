from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

def insert_journal_into_pinecone(user_id: str, title: str, thoughts: str):
    """
    Embeds and inserts a journal entry into Pinecone.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    # Use text_key="thought" for journals
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="thought")
    
    doc = Document(
        page_content=thoughts,
        metadata={
            "user_id": user_id,
            "title": title,
            "type": "journal"
        }
    )
    
    vectorstore.add_documents([doc])
    return {"status": "success", "message": "Journal entry inserted successfully"}

def insert_affirmation_into_pinecone(user_id: str, daily_affirmation: str):
    """
    Embeds and inserts an affirmation into Pinecone.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    # Use text_key="affirmation" for affirmations
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="affirmation")
    
    doc = Document(
        page_content=daily_affirmation,
        metadata={
            "user_id": user_id,
            "type": "affirmation"
        }
    )
    
    vectorstore.add_documents([doc])
    return {"status": "success", "message": "Affirmation inserted successfully"}


def insert_chat_history_into_pinecone(user_id: str, query: str, response: str):
    """
    Embeds and inserts a chat interaction (query + response) into Pinecone.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    # Use text_key="chat_history" for chat history
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="chat_history")
    
    # We store the combined interaction
    content = f"User: {query}\nAssistant: {response}"
    
    doc = Document(
        page_content=content,
        metadata={
            "user_id": user_id,
            "type": "chat_history"
        }
    )
    
    vectorstore.add_documents([doc])
    return {"status": "success", "message": "Chat history inserted successfully"}

def insert_tool_usage_into_pinecone(user_id: str, mood: str, mood_level: int, picked_tool: str):
    """
    Embeds and inserts a tool usage record into Pinecone.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    # Use text_key="mood" so we can search by mood later
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings, text_key="mood")
    
    doc = Document(
        page_content=mood,
        metadata={
            "user_id": user_id,
            "mood_level": mood_level,
            "picked_tool": picked_tool,
            "type": "tool_usage"
        }
    )
    
    vectorstore.add_documents([doc])
    return {"status": "success", "message": "Tool usage saved successfully"}

import os
from langchain_groq import ChatGroq

def get_llm(api_key):
    """
    Returns the Free Llama 3.3 model via Groq.
    """
    if not api_key:
        raise ValueError("Groq API Key is missing!")
        
    llm = ChatGroq(
        temperature=0, 
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile" 
    )
    return llm
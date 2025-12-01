import os
import json
import ollama

ollama_url = "http://localhost:11434/"


# Single turn chatbot - Query Ollama server using the Mistral model and return responses
'''def ollama_query(input_of_user: str, model_selected: str = "mistral") -> str:
    try:
        model_response = ollama.generate(
            model= model_selected,
            prompt=input_of_user,
            stream = False 
        )
        return model_response.get("response", "").strip()
    
    # This is when the Ollama server is unreachable
    except Exception as error:    
            return f"Error connnecting to ollama: {error}" '''


# Multi turn chatbot - Query Ollama server using the Mistral model and return responses
def ollama_query(input_of_user: str, model_selected: str = "mistral_q4km", stream: bool = False) -> str:
    try:
        model_response = ollama.generate(
            model= model_selected,
            prompt=input_of_user,
            stream = False 
        )
        return model_response.get("response", "").strip()
    
    # This is when the Ollama server is unreachable
    except Exception as error:    
            return f"Error connnecting to ollama: {error}" 




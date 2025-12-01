#import openai
#import requests

'''from src.ollama_client import ollama_query

def suggest_remediation(log: str) -> str:
    prompt = f"""
    Given this log:

    {log}
    Suggest an actionable remediation step.
    """

    return ollama_query(prompt, model_selected="mistral")'''

#response = openai.ChatCompletion.create(
        #model="gpt-4",
        #messages=[{"role": "user", "content": prompt}],
        #max_tokens=150
 #)
    #return response['choices'][0]['message']['content'].strip()

from src.ollama_client import ollama_query

def suggest_remediation(log: str) -> str:
    """
    Returns a concise remediation step for a given log using the Ollama model.
    """
    prompt = f"""
Given this security log:

{log}

Provide a clear, concise, and actionable remediation step that an SOC analyst should take.
"""

    try:
        # Use the correct argument name for your ollama_query function
        result = ollama_query(prompt, model_selected="mistral_q4km")
        if not result:
            return "No remediation returned by AI."
        return result
    except Exception as e:
        return f"Error generating remediation: {e}"

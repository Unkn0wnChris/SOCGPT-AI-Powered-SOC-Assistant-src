#import openai
from src.ollama_client import ollama_query 

def explain_threat(log: str, question: str) -> str:
    prompt = f"""
    Log:
    {log}

    Question:
    {question}
    """
    return ollama_query(prompt, model_selected="mistral:7b-instruct-q4_K_M")

   # response = openai.ChatCompletion.create(
   #    model="gpt-4",
   #     messages=[{"role": "user", "content": prompt}],
   #    max_tokens=200
   #)
   # return response['choices'][0]['message']['content'].strip()



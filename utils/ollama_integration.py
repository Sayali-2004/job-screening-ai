import ollama

DEFAULT_MODEL = "mistral"  # You can change this to "llama2", etc.

def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    try:
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content']
    except Exception as e:
        print("❌ Error calling Ollama:", e)
        return "Error: Could not generate response"

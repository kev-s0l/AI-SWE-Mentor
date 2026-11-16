import ollama

def generate_response(messages: list[dict[str,str]]) -> str:
    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages= messages
    )

    return response["message"]["content"]
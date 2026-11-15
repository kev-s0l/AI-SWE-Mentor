import ollama

# Generate a response from the local language model
# def generate_response(prompt: str) -> str:
#     response = ollama.chat(
#         model="qwen2.5-coder:7b",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response["message"]["content"]


def generate_response(messages: list[dict[str,str]]) -> str:
    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages= messages
    )

    return response["message"]["content"]
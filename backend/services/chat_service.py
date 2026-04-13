# EchoAI

# services/chat_service.py

from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

def generate_chat_response(messages, mode="general"):

    # 🎯 Model selection logic
    if mode == "general":
        model = "llama3:latest"
        temperature = 0.7
        max_tokens = 500

    elif mode == "fast":
        model = "phi3:mini"
        temperature = 0.6
        max_tokens = 300

    else:
        model = "phi3:mini"

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                full_response += delta.content

        return full_response

    except Exception as e:
        return f"Error generating response: {str(e)}"
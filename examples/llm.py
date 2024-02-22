from jarvisbot import JarvisBot

client = JarvisBot(
    api_key="123",
    base_url="http://441913d655fe469ef4.jarvisbot.live/llmapi/v1",
)
messages = [
    {
        "content": "You are a helpful assistant.",
        "role": "system"
    },
    {
        "content": "What is the capital of France?",
        "role": "user"
    }
]

completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    max_tokens=512,
    temperature=0.6,
    top_p=0.8,
    top_k=0.0,
    stream=False,
    presence_penalty=0,
    frequency_penalty=0,
    repetition_penalty=1.1,
    seed=-1
)
print(f"Prompt: {messages}")
print(completion.choices[0].message.content.strip())

import ollama
import openai

answer = ollama.generate(model='deepseek-r1', prompt='你是谁')
print(ollama.list())

res1 = ollama.chat(model='deepseek-r1', messages=[{'role': 'user', 'content': '你是谁'}])
print(res1.message.content)
res2 = ollama.chat(model='deepseek-r1', messages=[{'role': 'user', 'content': '你到底是谁'}])
print(res2.message.content)


client = openai.OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
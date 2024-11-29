from openai import OpenAI 
import os
import dotenv

dotenv.load_dotenv()
API_KEY_CHATGPT=os.getenv('API_KEY_CHATGPT')
client=OpenAI()
MINI="gpt-4o-mini"
WHISPER="whisper-1"
audio_file=open("Audio1.mp3", "rb") transcript=client.audio.transcriptions.create( model=WHISPER, file=audio_file, prompt="Traduce everything clear. In the last part, add a good prompt that preserve the context of the audio"

)
texto=input("if you want the IA has a prompt for answer better write something")
if texto=="":
    texto="You have to answer the question and make helping suggestions for the task"

stream = client.chat.completions.create(
    model=MINI,
    messages=[
        {"role":"system", "content": texto},
        {"role": "user", "content": audio_file}
    ],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
"""
completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "assistant", "content": "You are a helpful assistant. Help me with my math homework!"}, # <-- This is the system message that provides context to the model
    {"role": "user", "content": "Hello! Could you solve 2+2?"}  # <-- This is the user message for which the model will generate a response
  ]
)
"""



#print("Assistant: " + completion.choices[0].message.content)

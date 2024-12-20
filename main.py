
from openai import OpenAI 
import os
import dotenv
import time


dotenv.load_dotenv()
client=OpenAI(api_key=os.environ.get("API_KEY_CHATGPT"))

audio_file= open("grabacion.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  prompt="The audio is always a order that you have to traduce clear",
  response_format="text",
  temperature=0.2
)
print(transcription)

with open("orden.txt", "w") as archivo:
    texto = transcription
    archivo.write(texto)

#Assistant read the file
file = client.files.create(
  file=open('orden.txt',"rb"),
  purpose='assistants',
)

# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  instructions="You are teacher of Artificial Intelligense. Explain what is AI, give sources for investigation and answer the questions",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

#Prove the first thread 
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Answer the question, and give sources for searching",
      "file_ids": [file.id]
    }
  ]
)

#Make the run client 
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

messages = client.beta.threads.messages.list(thread_id=thread.id)


while True:
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    try:
        #See if image has been created
        messages.data[0].content[0].image_file
        #Sleep to make sure run has completed
        time.sleep(20)
        print('Question solved')
        break
    except:
        time.sleep(10)
        print('Assistant still working...')

response = client.images.generate(
  model="dall-e-3",
  prompt="Represent a great class of AI",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

# Descargar y guardar la imagen
image_name = "teacher_ai_class.png"  # Nombre del archivo para guardar la imagen
response_image = requests.get(image_url)

if response_image.status_code == 200:  # Verificar que la descarga fue exitosa
    with open(image_name, "wb") as img_file:
        img_file.write(response_image.content)
    print(f"Imagen guardada como {image_name}")
else:
    print(f"Error al descargar la imagen. Código de estado: {response_image.status_code}")

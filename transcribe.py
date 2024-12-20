from openai import OpenAI 
import os
import dotenv
import time
import requests



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



completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are teacher of Artificial Intelligense."},
        {
            "role": "user",
            "content": "Explain what is AI, give sources for investigation and answer the questions"
        }
    ]
)
chat_response=completion.choices[0].message
print(completion.choices[0].message)

texto=chat_response.content
with open("output_class.txt", "w") as archivo:
    archivo.write(texto)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a teacher of AI that have to answer the question of your student."},
        {
            "role": "user",
            "content": transcription
        }
    ]
)

chat_answer=completion.choices[0].message
print(completion.choices[0].message)

texto=chat_answer.content
with open("output_question.txt", "w") as archivo:
    archivo.write(texto)


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

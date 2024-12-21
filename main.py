from openai import OpenAI 
import os
import dotenv
import time
import requests
import grabar_audio



dotenv.load_dotenv()
client=OpenAI(api_key=os.environ.get("API_KEY_CHATGPT"))



grabar_audio.grabar_audio()

try:
    audio_file= open("grabacion.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    prompt="if you have problems write problem, no more",
    response_format="text",
    temperature=0.2
    )
except ValueError:
    valor_cambio=False
    print("Error: "+ValueError)


print(transcription)

if transcription=="problem" or transcription=="":
    print("No hay peticiones")
    

else: 
    with open("orden.txt", "w") as archivo:
        texto = transcription
        archivo.write(texto)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You have to answare the question with presition, information's sources and like a professional in the field"},
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
        prompt="Represent the answare of:"+transcription,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # Descargar y guardar la imagen
    image_name = "image_question.png"  # Nombre del archivo para guardar la imagen
    response_image = requests.get(image_url)

    if response_image.status_code == 200:  # Verificar que la descarga fue exitosa
        with open(image_name, "wb") as img_file:
            img_file.write(response_image.content)
        print(f"Imagen guardada como {image_name}")
    else:
        print(f"Error al descargar la imagen. Código de estado: {response_image.status_code}")
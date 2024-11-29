from openai import OpenAI
client = OpenAI()

audio_file= open("audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  prompt="You have to consider the time of the task, and if it is a event or just a question of a work",
  response_format="text",
  temperature=0.2
)
print(transcription.text)
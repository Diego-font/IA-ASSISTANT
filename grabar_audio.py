import pyaudio
import wave

# Configuración de los parámetros de grabación
FORMATO = pyaudio.paInt16      # Formato de audio de 16 bits
CANAL = 1                       # Canal mono (1 para mono, 2 para estéreo)
RATE = 44100                    # Frecuencia de muestreo en Hz
CHUNK = 1024                    # Tamaño del buffer
DURACION = 10                    # Duración de la grabación en segundos
NOMBRE_ARCHIVO = "grabacion.wav"  # Nombre del archivo de salida

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Configurar la entrada de audio
stream = audio.open(format=FORMATO, channels=CANAL, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Grabando...")

# Almacenar los fragmentos de audio grabados
frames = []
for _ in range(int(RATE / CHUNK * DURACION)):
    data = stream.read(CHUNK)
    frames.append(data)

# Finalizar la grabación
print("Grabación completada.")
stream.stop_stream()
stream.close()
audio.terminate()

# Guardar la grabación en un archivo .wav
with wave.open(NOMBRE_ARCHIVO, "wb") as wf:
    wf.setnchannels(CANAL)
    wf.setsampwidth(audio.get_sample_size(FORMATO))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Archivo guardado como {NOMBRE_ARCHIVO}")

import pyaudio
# Configurações
FORMAT = pyaudio.paInt16  # Áudio 16 bits
CHANNELS = 1              # Mono
RATE = 44100              # 44.1 kHz
CHUNK = 1024              # Blocos de leitura

# Inicializa
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
print(" Gravando... (Ctrl+C para parar)")
try:
    while True:
        data = stream.read(CHUNK)
        # Aqui você poderia salvar, enviar pela rede, processar, etc.
except KeyboardInterrupt:
    print("\nParando...")
# Fecha
stream.stop_stream()
stream.close()
audio.terminate()

from flask import Flask, request
import cv2
import numpy as np
app = Flask(__name__)
@app.route("/stream", methods=["POST"])
def receber_stream():
    video_file = request.files["video"]
    audio_file = request.files["audio"]
    # Vídeo
    npimg = np.frombuffer(video_file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imshow("Video Recebido", frame)
    cv2.waitKey(1)
    # Áudio
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())
    return "ok"
app.run(host="0.0.0.0", port=5000)

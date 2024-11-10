from flask import Flask, request, jsonify
import tempfile
import cv2
from ultralytics import YOLO
# (Inclua o código de processamento de vídeo aqui)

app = Flask(__name__)

@app.route('/process_video', methods=['POST'])
def process_video():
    video_file = request.files['video']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        video_file.save(temp_video_file.name)
        temp_video_path = temp_video_file.name

    # Realize o processamento com YOLO no vídeo
    # (Coloque o código de processamento de vídeo aqui)

    return jsonify({"status": "success", "message": "Video processed successfully."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
import os
import gc
import cv2
import tempfile
from minio import Minio
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Configurações do MinIO
MINIO_URL = "minio:9000"  # URL do MinIO
ACCESS_KEY = "minio"  # Chave de acesso do MinIO
SECRET_KEY = "minio123"  # Chave secreta do MinIO
BUCKET_NAME = "frames"  # Nome do bucket MinIO
IMAGE_NAME = "images.jpeg"  # Caminho da imagem no MinIO

# Inicialize o cliente MinIO
minio_client = Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Defina como True se estiver usando HTTPS
)

# Caminho do modelo YOLO local
model_path = "yolov8n.pt"

# Baixe o modelo apenas se ele não existir localmente
if not os.path.exists(model_path):
    model = YOLO("yolov8n.pt")
else:
    model = YOLO(model_path)

# Nome do arquivo de vídeo no bucket "frame"
video_name = "1107.mp4"
response = minio_client.get_object("frames", video_name)
video_data = response.read()

# Salve o vídeo temporariamente
with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
    temp_video_file.write(video_data)
    temp_video_path = temp_video_file.name

# Abra o vídeo com OpenCV
cap = cv2.VideoCapture(temp_video_path)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(temp_video_path.replace(".mp4", "_annotated.mp4"), fourcc, cap.get(cv2.CAP_PROP_FPS),
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Processa cada quadro do vídeo
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Realiza a detecção no quadro
    results = model(frame)

    # Anote o quadro com as detecções
    annotated_frame = results[0].plot()

    # Escreve o quadro anotado no novo vídeo
    out.write(annotated_frame)

# Libera recursos
cap.release()
out.release()
gc.collect()

# Upload do vídeo anotado para o bucket "bronze"
annotated_video_path = temp_video_path.replace(".mp4", "_annotated.mp4")
with open(annotated_video_path, "rb") as file_data:
    minio_client.put_object(
        "bronze",  # Bucket de destino
        os.path.basename(annotated_video_path),  # Nome do arquivo
        file_data,
        length=os.path.getsize(annotated_video_path),
        content_type="video/mp4"
    )

# Remove arquivos temporários
os.remove(temp_video_path)
os.remove(annotated_video_path)

# Liberar o modelo do YOLO
del model
gc.collect()

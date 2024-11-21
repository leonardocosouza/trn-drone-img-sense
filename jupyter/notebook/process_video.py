import os
import gc
import cv2
import tempfile
from minio import Minio
from minio.commonconfig import CopySource
from ultralytics import YOLO

# Configurações do MinIO
MINIO_URL = "minio:9000"  # URL do MinIO
ACCESS_KEY = "minio"      # Chave de acesso do MinIO
SECRET_KEY = "minio123"   # Chave secreta do MinIO
BUCKET_SOURCE = "frames"  # Nome do bucket fonte
BUCKET_DEST = "bronze"    # Nome do bucket destino
BUCKET_LANDING = "landing"  # Nome do bucket para arquivos processados

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

# Listar objetos no bucket fonte
objects = minio_client.list_objects(BUCKET_SOURCE, recursive=True)

for obj in objects:
    if obj.object_name.endswith(".mp4"):
        print(f"Processando vídeo: {obj.object_name}")

        # Baixar o vídeo do bucket
        response = minio_client.get_object(BUCKET_SOURCE, obj.object_name)
        video_data = response.read()

        # Salvar o vídeo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            temp_video_file.write(video_data)
            temp_video_path = temp_video_file.name

        # Processar o vídeo com OpenCV
        cap = cv2.VideoCapture(temp_video_path)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        annotated_video_path = temp_video_path.replace(".mp4", "_annotated.mp4")
        out = cv2.VideoWriter(
            annotated_video_path,
            fourcc,
            cap.get(cv2.CAP_PROP_FPS),
            (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        )

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

        # Upload do vídeo anotado para o bucket destino
        with open(annotated_video_path, "rb") as file_data:
            minio_client.put_object(
                BUCKET_DEST,  # Bucket de destino
                os.path.basename(annotated_video_path),  # Nome do arquivo
                file_data,
                length=os.path.getsize(annotated_video_path),
                content_type="video/mp4"
            )

        # Mover o arquivo original para o bucket "landing"
        copy_source = CopySource(BUCKET_SOURCE, obj.object_name)
        minio_client.copy_object(
            BUCKET_LANDING,
            obj.object_name,
            copy_source
        )
        minio_client.remove_object(BUCKET_SOURCE, obj.object_name)

        # Remove arquivos temporários
        os.remove(temp_video_path)
        os.remove(annotated_video_path)

        print(f"Vídeo processado e enviado: {os.path.basename(annotated_video_path)}")

# Liberar o modelo do YOLO
del model
gc.collect()

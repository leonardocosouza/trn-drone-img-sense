import os
import gc
import cv2
import tempfile
from minio import Minio
from ultralytics import YOLO


# Configurações do MinIO
MINIO_URL = "minio:9000"  # URL do MinIO
ACCESS_KEY = "minio"      # Chave de acesso do MinIO
SECRET_KEY = "minio123"   # Chave secreta do MinIO
BUCKET_NAME = "frames"    # Nome do bucket MinIO
LANDING_BUCKET = "landing"  # Bucket para arquivos processados

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

# Listar todos os objetos no bucket "frames"
objects = minio_client.list_objects(BUCKET_NAME)

for obj in objects:
    try:
        print(f"Processando: {obj.object_name}")

        # Baixar o objeto do bucket
        response = minio_client.get_object(BUCKET_NAME, obj.object_name)
        image_data = response.read()

        # Salvar a imagem temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
            temp_image_file.write(image_data)
            temp_image_path = temp_image_file.name

        # Realizar a detecção na imagem
        results = model(temp_image_path)

        # Salvar a imagem anotada localmente
        annotated_image = results[0].plot()
        annotated_image_path = temp_image_path.replace(".jpg", "_annotated.jpg")
        cv2.imwrite(annotated_image_path, annotated_image)

        # Fazer o upload da imagem anotada para o bucket "bronze"
        with open(annotated_image_path, "rb") as file_data:
            minio_client.put_object(
                "bronze",  # Nome do bucket de destino
                os.path.basename(annotated_image_path),  # Nome do arquivo no MinIO
                file_data,
                length=os.path.getsize(annotated_image_path),
                content_type="image/jpeg"
            )

        # Mover o arquivo original para o bucket "landing"
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file.seek(0)

            # Fazer upload no bucket "landing"
            minio_client.put_object(
                LANDING_BUCKET,
                obj.object_name,  # Mesmo nome no bucket "landing"
                temp_file,
                length=len(image_data),
                content_type="image/jpeg"
            )

        # Excluir o arquivo original do bucket "frames"
        minio_client.remove_object(BUCKET_NAME, obj.object_name)
        print(f"Arquivo movido para o bucket {LANDING_BUCKET}: {obj.object_name}")

        # Remover arquivos temporários locais
        os.remove(temp_image_path)
        os.remove(annotated_image_path)

    except Exception as e:
        print(f"Erro ao processar {obj.object_name}: {e}")

# Liberar o modelo e forçar a coleta de lixo para liberar memória
del model
gc.collect()

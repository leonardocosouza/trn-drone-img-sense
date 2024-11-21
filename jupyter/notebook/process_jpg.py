import os
import gc
import cv2
import tempfile
from minio import Minio
from ultralytics import YOLO
import matplotlib.pyplot as plt


# Configurações do MinIO
MINIO_URL = "minio:9000"  # URL do MinIO
ACCESS_KEY = "minio"        # Chave de acesso do MinIO
SECRET_KEY = "minio123"        # Chave secreta do MinIO
BUCKET_NAME = "frames"      # Nome do bucket MinIO
IMAGE_NAME = "images.jpeg"  # Caminho da imagem no MinIO

# Inicialize o cliente MinIO
minio_client = Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Defina como True se estiver usando HTTPS
)

# Baixe a imagem do MinIO
response = minio_client.get_object(BUCKET_NAME, IMAGE_NAME)
image_data = response.read()

# Salve a imagem temporariamente
with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
    temp_image_file.write(image_data)
    temp_image_path = temp_image_file.name

# Caminho do modelo YOLO local
model_path = "yolov8n.pt"

# Baixe o modelo apenas se ele não existir localmente
if not os.path.exists(model_path):
    # Carregar o modelo YOLO e salvar localmente para evitar downloads repetidos
    model = YOLO("yolov8n.pt")
else:
    model = YOLO(model_path)

# Realize a detecção na imagem baixada
results = model(temp_image_path)

# Exiba os resultados e converta a imagem anotada para RGB para exibição com Matplotlib
# annotated_image = results[0].plot()  # .plot() gera a imagem anotada com as deteções
# annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

# Exiba os resultados e salve a imagem anotada localmente
annotated_image = results[0].plot()
annotated_image_path = temp_image_path.replace(".jpg", "_annotated.jpg")
cv2.imwrite(annotated_image_path, annotated_image)

# Liberar o modelo e forçar a coleta de lixo para liberar memória
del model
gc.collect()


# Faça o upload da imagem anotada para o bucket "bronze"
with open(annotated_image_path, "rb") as file_data:
    minio_client.put_object(
        "bronze",  # Nome do bucket de destino
        os.path.basename(annotated_image_path),  # Nome do arquivo no MinIO
        file_data,
        length=os.path.getsize(annotated_image_path),
        content_type="image/jpeg"
    )


# Exibir a imagem no notebook usando Matplotlib
# plt.imshow(annotated_image_rgb)
# plt.axis('off')  # Remove os eixos
# plt.show()

# Remova o arquivo temporário
os.remove(temp_image_path)

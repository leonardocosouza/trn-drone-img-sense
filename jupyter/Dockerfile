# Base da imagem com Python 3.8
FROM python:3.8

# Instala o git e atualiza o pip
RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip
RUN apt-get install libgl1 -y

# Clona o YOLOv7 e instala as dependências
RUN git clone https://github.com/WongKinYiu/yolov7.git
WORKDIR /yolov7
RUN pip install -r requirements.txt

# Instala o Jupyter Notebook
RUN pip install jupyter

RUN pip install flask
COPY process_video.py /app/process_video.py

# Expõe a porta padrão do Jupyter Notebook
EXPOSE 8816

# Comando para iniciar o Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8816", "--no-browser", "--allow-root", "--NotebookApp.disable_check_xsrf=True". "python", "/app/process_video.py"]

###docker build -t yolov7-jupyter .

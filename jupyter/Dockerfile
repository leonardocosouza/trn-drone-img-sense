# Base da imagem com Python 3.8
FROM python:3.8

# Instala o git, atualiza o pip e instala dependências adicionais
RUN apt update && apt install -y git openssh-server libgl1
RUN pip install --upgrade pip
RUN apt install expect -y

RUN pip install ultralytics minio opencv-python matplotlib


# Configura e inicia o servidor SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd  # Define uma senha para o root (substitua por uma senha segura)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Cria um usuário yolo_user para acesso via SSH
RUN useradd -ms /bin/bash nifi && echo "nifi:password" | chpasswd  # Substitua a senha por algo seguro
RUN echo "nifi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Expor a porta para SSH
EXPOSE 22

# Clona o YOLOv7 e instala as dependências
RUN git clone https://github.com/WongKinYiu/yolov7.git
WORKDIR /yolov7
RUN pip install -r requirements.txt

# Instala o Jupyter Notebook
RUN pip install jupyter

# Cria o diretório notebook
RUN mkdir -p /app/notebook

# Expõe a porta padrão do Jupyter Notebook
EXPOSE 8816

# Iniciar o servidor SSH e o Jupyter Notebook
CMD sh -c "/usr/sbin/sshd -D & jupyter notebook --ip=0.0.0.0 --port=8816 --no-browser --allow-root --NotebookApp.disable_check_xsrf=True"

#docker build -t yolov7-jupyter .

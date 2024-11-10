

parar e deletar todos os containers e deletar volumes
docker stop $(docker ps -q) && docker rm $(docker ps -a -q) && docker volume rm $(docker volume ls -q) && docker volume rm $(docker volume ls -q)


deletar todas as imagens
docker rmi $(docker images -a -q)




1. Verifique se o Jupyter Notebook Está Instalado
Tente rodar o seguinte comando para confirmar se o Jupyter Notebook está instalado:
````
jupyter notebook --version
````
Se o comando acima retornar um erro, você precisa instalar o Jupyter Notebook.

2. Instale o Jupyter Notebook
Para instalar o Jupyter Notebook, execute:
````
pip install notebook
````
Se estiver usando Python 3 e o comando pip está associado ao Python 2, tente:
````
pip3 install notebook
````
3. Reinicie o Comando Jupyter
Após instalar o Jupyter Notebook, execute o comando novamente:
````
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser
````



sudo apt-get install libgl1 -y
!pip install ultralytics
!pip install minio


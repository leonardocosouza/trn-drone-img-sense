# Drones - Classificação de Imagens


![/docs/capa.png](docs%2Fcapa.png)

### Requisitos
1. [**Instalação do Docker em uma VM Ubuntu no Google Cloud**](docs/instalando-docker.md)
2. [**Criando uma Regra de Firewall no Google Cloud para Liberar a Porta**](docs/regra-firewall.md)
3. [**Clonando um Repositório Git**](docs/git-clone.md)

## Executando o Docker Compose e Verificando os Contêineres

Inicie os Contêineres com Docker Compose

Execute o comando abaixo para iniciar todos os contêineres definidos no docker-compose.yml:
````
sudo docker-compose up -d
````
O argumento -d faz com que o Docker Compose execute os contêineres em segundo plano (modo detached).

Para listar todos os contêineres em execução, use:
```
sudo docker ps
```
![/docks/Dockerps.png](docs%2FDockerps.png)

**Observação: O contêiner minio-mc é responsável por criar os buckets no MinIO e, em seguida, se torna indisponível.**


## Configuração do App DJI Fly

<p align="left">
  <img src="/docs/Screenshot_20241106_201650.jpg" width="700">
</p>

<p align="left">
  <img src="/docs/Screenshot_20241106_201657.jpg" width="700">
</p>

**Adicine o IP Externo da VM**
<p align="left">
  <img src="/docs/Screenshot_20241106_201621.jpg" width="700">
</p>

**Clique em "Iniciar"**

<p align="left">
  <img src="/docs/Screenshot_20241106_201641.jpg" width="700">
</p>


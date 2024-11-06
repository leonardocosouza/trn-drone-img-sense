# eVTOLs - Electric Vertical Take-Off and Landing - Quem estará no Controle?


![/docs/capa.png](docs%2Fcapa.png)

- [**Instalação do Docker em uma VM Ubuntu no Google Cloud**](docs/instalando-docker.md)
- [**Criando uma Regra de Firewall no Google Cloud para Liberar a Porta**](docs/regra-firewall.md)
- [**Clonando um Repositório Git**](docs/git-clone.md)

## Executando o Docker Compose e Verificando os Contêineres

Inicie os Contêineres com Docker Compose

Execute o comando abaixo para iniciar todos os contêineres definidos no docker-compose.yml:
````
docker-compose up -d
````
O argumento -d faz com que o Docker Compose execute os contêineres em segundo plano (modo detached).

Para listar todos os contêineres em execução, use:
```
docker ps
```
![/docks/Dockerps.png](docs%2FDockerps.png)

**Observação: O contêiner minio-mc é responsável por criar os buckets no MinIO e, em seguida, se torna indisponível.**


Configuração do App DJI Fly



![/docs/Screenshot_20241106_201621.jpg](docs%2FScreenshot_20241106_201621.jpg)

![/docs/Screenshot_20241106_201641.jpg](docs%2FScreenshot_20241106_201641.jpg)

![/docs/Screenshot_20241106_201650.jpg](docs%2FScreenshot_20241106_201650.jpg)

![/docs/Screenshot_20241106_201657.jpg](docs%2FScreenshot_20241106_201657.jpg)
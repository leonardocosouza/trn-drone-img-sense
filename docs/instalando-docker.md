
# Instalação do Docker em uma VM Ubuntu no Google Cloud

Este guia detalha os passos para instalar o Docker em uma instância de VM Ubuntu no Google Cloud.

**1. Conecte-se à VM no Google Cloud**

No Google Cloud Console, vá para Compute Engine > Instâncias de VM.
Encontre sua VM com Ubuntu e clique em Conectar via SSH para abrir um terminal conectado à VM.

**2. Atualize o Sistema**
Atualize os pacotes da VM para garantir que o sistema está atualizado:
```
sudo apt update
sudo apt upgrade -y
```
**3. Instale Dependências Necessárias**
Instale pacotes necessários para o Docker:
```
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

**4. Adicione o Repositório Oficial do Docker** 
Adicione a chave GPG do Docker:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
Adicione o repositório Docker ao sistema:
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
**5. Instale o Docker**
```
sudo apt update
```
Instale o Docker:
```
sudo apt install -y docker-ce
```
**6. Verifique a Instalação do Docker**
Execute o comando abaixo para verificar se o Docker foi instalado corretamente:
```
sudo docker --version
```
**7. (Opcional) Permita que o Usuário Utilize o Docker sem sudo**
Adicione o usuário atual ao grupo docker para permitir o uso de comandos Docker sem sudo:
```
sudo usermod -aG docker $USER
```
Nota: Reinicie a sessão SSH para aplicar as mudanças.

**8. Teste a Instalação**
Execute o comando abaixo para verificar se o Docker está funcionando corretamente:
```
docker run hello-world
```
Esse comando irá baixar e executar uma imagem de teste do Docker. Se a instalação estiver correta, você verá uma mensagem de boas-vindas do Docker.

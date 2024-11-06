
# Clonando um Repositório Git
Este guia descreve os passos para clonar o repositório Git na VM.

Pré-requisitos
Certifique-se de que a VM possui o Git instalado. Para verificar, execute o comando:
```
git --version
```
Se o Git não estiver instalado, você pode seguir as instruções para instalação no site oficial: [Git - Downloads] (https://git-scm.com/downloads).

**1. Obtenha a URL do repositório Git:**

No GitHub (ou outra plataforma de hospedagem Git), vá até a página do repositório que você deseja clonar.
Clique no botão Code e copie a URL (HTTPS ou SSH) fornecida.

**2. No Terminal:**

Navegue até o diretório onde deseja clonar o repositório. Por exemplo, para acessar a pasta Projetos:
````
cd ~/Projetos
````
**3. Clone o Repositório:**

No terminal, execute o comando abaixo:
```
git clone https://github.com/leonardocosouza/trn-drone-img-sense.git
```
**4. Acesse o Diretório Clonado:**
```
cd trn-drone-img-sense
```

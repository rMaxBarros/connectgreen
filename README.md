# Projeto - Cidades ESGInteligentes: ConnectGreen

Este projeto implementa a API para a plataforma "ConectaVerde", uma solução focada em sustentabilidade urbana, utilizando um pipeline DevOps completo para automação de build, teste e deploy.

## Como executar localmente com Docker

1.  **Pré-requisitos:** Certifique-se de ter o Docker Desktop instalado e em execução no seu computador.
2.  **Clonar:** Clone este repositório: `git clone https://github.com/rMaxBarros/connectgreen.git`
3.  **Navegar:** Entre na pasta do projeto: `cd connectgreen`
4.  **Subir os Serviços:** Execute o comando `docker compose up --build -d`. Ele construirá a imagem da aplicação e iniciará os contêineres da API (`connectgreen`) e do banco de dados (`mongodb`) em segundo plano.
5.  **Aguardar:** Espere cerca de 20-30 segundos para os serviços iniciarem completamente.
6.  **Verificar API:** Acesse `http://localhost:5000` no seu navegador. Você deve ver a mensagem: `API ConnectGreen no ar! Acesse /usuarios para ver os dados.`
7.  **Verificar Dados (Opcional):** Se você populou o banco de dados localmente (conforme instruções anteriores), acesse `http://localhost:5000/usuarios` para ver os dados JSON.
Utilizamos o **GitHub Actions** para automatizar o ciclo de vida da aplicação, garantindo integração e entrega contínuas.

* **Entrega Contínua (CD):**
    * **Arquivo:** `.github/workflows/cd_pipeline.yml`
    * **Gatilho:** Acionado a cada *push* (merge ou commit direto) na branch `main`.
    * **Etapas:**
        1.  Checkout do código.
        2.  Login no Docker Hub (usando `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` dos Secrets).
        3.  Build da imagem Docker da aplicação (`connectgreen`) e push para o Docker Hub (`rmaxbarros/connectgreen:latest`).
        4.  Deploy da imagem recém-publicada para o **Azure Web App** (usando o `AZURE_WEBAPP_PUBLISH_PROFILE` dos Secrets).
    * **Objetivo:** Automatizar a publicação de uma nova versão funcional da aplicação no ambiente de produção (Azure) após a integração bem-sucedida na `main`.

## Containerização

A aplicação foi containerizada usando Docker para garantir consistência entre os ambientes de desenvolvimento, teste e produção.

* **Dockerfile:**
    * Define a imagem da aplicação Flask.
    * Utiliza uma imagem base `python:3.9-slim`.
    * Copia o `requirements.txt` e instala as dependências via `pip`.
    * Copia o código da aplicação (`app.py`).
    * Expõe a porta `5000`.
    * Define o comando de inicialização `flask run`.

    ```dockerfile
    # Etapa 1: Define a imagem base com Python
    FROM python:3.9-slim

    # Etapa 2: Define o diretório de trabalho dentro do container
    WORKDIR /app

    # Etapa 3: Copia o arquivo de dependências e instala as bibliotecas
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Etapa 4: Copia o resto dos arquivos da aplicação
    COPY . .

    # Etapa 5: Expõe a porta que a aplicação vai usar
    EXPOSE 5000

    # Etapa 6: Comando para iniciar a aplicação quando o container for executado
    CMD ["flask", "run", "--host=0.0.0.0"]
    ```

* **Docker Compose (`docker-compose.yml`):**
    * Orquestra os serviços `webapp` (aplicação Flask) e `mongodb`.
    * Define a build da `webapp` a partir do `Dockerfile`.
    * Mapeia a porta `5000` do host para a `5000` do contêiner da aplicação.
    * Configura a variável de ambiente `MONGO_URI` para a aplicação se conectar ao serviço `mongodb` na rede interna do Docker.
    * Utiliza a imagem oficial `mongo:latest` para o banco de dados.
    * Mapeia a porta `27017` para acesso externo (via Compass).
    * Define um volume (`mongodb_data`) para persistir os dados do MongoDB.

    ```yaml
    version: '3.8'

    services:
      webapp:
        build: .
        container_name: connectgreen # Nome amigável alterado
        ports:
          - "5000:5000"
        volumes:
          - .:/app
        environment:
          - FLASK_APP=app.py
          - FLASK_ENV=development
          - MONGO_URI=mongodb://mongodb:27017/conectaVerdeDB
        depends_on:
          - mongodb

      mongodb:
        image: mongo:latest
        container_name: mongodb
        ports:
          - "27017:27017"
        volumes:
          - mongodb_data:/data/db

    volumes:
      mongodb_data:
    ```

## Prints do Funcionamento

**1. Aplicação rodando localmente com Docker:**
<img width="1919" height="1018" alt="Captura de tela 2025-10-10 160925" src="https://github.com/user-attachments/assets/3a4f1ba7-a9b7-4193-9def-96e7aa3e26dd" />


**2. Pipeline de CI/CD executado com sucesso no GitHub Actions:**
<img width="1919" height="823" alt="Captura de tela 2025-10-10 183328" src="https://github.com/user-attachments/assets/7bb9cc23-54d2-4541-9c5f-c96a17cd5cf0" />


**3. Aplicação em produção no Azure:**
<img width="1039" height="131" alt="Captura de tela 2025-10-10 183832" src="https://github.com/user-attachments/assets/caf451df-18b5-4fa6-80f9-3624f7db3344" />

**4. Testes Automatizados BDD Passando Localmente (`pytest`):**
<img width="1919" height="1079" alt="1" src="https://github.com/user-attachments/assets/be62a231-9af7-470d-9de7-313ff95b41fd" />

**5. Pipeline de CI no Pull Request (GitHub Actions):**
<img width="1919" height="1028" alt="2" src="https://github.com/user-attachments/assets/57f207ee-b574-4b46-9e07-5f45d6b9d47e" />

**6. Aplicação em Produção no Azure Web App:**
<img width="1165" height="431" alt="Captura de tela 2025-10-21 203623" src="https://github.com/user-attachments/assets/924a47bd-c5c5-4cee-81b8-cffc4f5bd905" />



## Tecnologias Utilizadas

* **Linguagem:** Python 3.9
* **Framework Web:** Flask
* **Banco de Dados:** MongoDB
* **Containerização:** Docker, Docker Compose
* **Testes Automatizados:** Pytest, Pytest-BDD (Gherkin), Requests, JSONSchema
* **CI/CD:** GitHub Actions
* **Nuvem (PaaS):** Microsoft Azure (Web App for Containers)
* **Controle de Versão:** Git, GitHub
* **Editor:** Visual Studio Code

# Projeto - Cidades ESGInteligentes: ConnectGreen

Este projeto implementa a API para a plataforma "ConectaVerde", uma solução focada em sustentabilidade urbana, utilizando um pipeline DevOps completo para automação de build, teste e deploy.

## Como executar localmente com Docker

1.  Certifique-se de ter o Docker Desktop instalado e em execução.
2.  Clone este repositório para a sua máquina local.
3.  Abra um terminal na raiz do projeto.
4.  Execute o comando `docker-compose up --build`.
5.  Aguarde os containers da aplicação e do banco de dados iniciarem.
6.  Acesse `http://localhost:5000` no seu navegador para verificar se a API está no ar.

## Pipeline CI/CD

Utilizamos o **GitHub Actions** para automatizar nosso ciclo de vida, conforme as práticas DevOps. O pipeline está dividido em:

* **Integração Contínua (CI):** O workflow `ci_pipeline.yml` é acionado a cada *pull request* para a branch `main`. Ele constrói o ambiente Docker e executa um teste de conectividade para garantir que novas alterações não quebrem a aplicação.
* **Entrega Contínua (CD):** O workflow `cd_pipeline.yml` é acionado a cada *push* na branch `main`. Ele constrói a imagem Docker da aplicação, a envia para o Docker Hub e, em seguida, realiza o deploy automático da nova imagem para o ambiente de produção no Azure Web App.

## Containerização

A aplicação foi containerizada usando Docker para garantir consistência entre os ambientes de desenvolvimento, teste e produção.

* **Dockerfile:** A imagem da aplicação é construída a partir de uma base Python, instalando as dependências listadas no `requirements.txt` e configurando o Flask para rodar.
* **Docker Compose:** O arquivo `docker-compose.yml` orquestra dois serviços: a `webapp` (nossa aplicação) e o `mongodb`. Ele configura a rede interna para que a aplicação possa se conectar ao banco de dados e gerencia os volumes para persistência dos dados.

## Prints do Funcionamento

**1. Aplicação rodando localmente com Docker:**
<img width="1919" height="1018" alt="Captura de tela 2025-10-10 160925" src="https://github.com/user-attachments/assets/3a4f1ba7-a9b7-4193-9def-96e7aa3e26dd" />


**2. Pipeline de CI/CD executado com sucesso no GitHub Actions:**
<img width="1919" height="823" alt="Captura de tela 2025-10-10 183328" src="https://github.com/user-attachments/assets/7bb9cc23-54d2-4541-9c5f-c96a17cd5cf0" />


**3. Aplicação em produção no Azure:**
<img width="1039" height="131" alt="Captura de tela 2025-10-10 183832" src="https://github.com/user-attachments/assets/caf451df-18b5-4fa6-80f9-3624f7db3344" />


## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** Flask
* **Banco de Dados:** MongoDB
* **Containerização:** Docker, Docker Compose
* **CI/CD:** GitHub Actions
* **Nuvem:** Microsoft Azure (WebApp for Containers)
* **Controle de Versão:** Git / GitHub

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
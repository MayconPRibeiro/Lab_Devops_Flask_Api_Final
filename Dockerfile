# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt requirements.txt

# Instalar dependências
RUN pip install -r requirements.txt

# Copiar os arquivos da API para o container
COPY . .

# Expor a porta 10000
EXPOSE 10000

# Comando para rodar a aplicação
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]

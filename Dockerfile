# Use uma imagem base com o Python
FROM python:3.8-slim

# Instale dependências
RUN pip install flask google-cloud-bigquery

# Copie o código da aplicação
COPY main.py /app/main.py
WORKDIR /app

# Execute a aplicação
CMD ["python", "main.py"]

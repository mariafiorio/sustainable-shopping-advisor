FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app.py .

# Variáveis de ambiente
ENV HOST=0.0.0.0
ENV PORT=5001
ENV DEBUG=False

# Porta exposta
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Comando de execução
CMD ["python", "app.py"]
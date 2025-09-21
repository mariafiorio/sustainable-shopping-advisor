#!/bin/bash
set -e

echo "🎯 Fazendo deploy do RecommenderAgent"

# Navegar para o diretório do agente
cd /Users/maria/microservices-demo/src/recommender-agent

# Build da imagem Docker
echo "🐳 Construindo imagem Docker..."
docker build -t recommender-agent:latest .

# Verificar se a imagem foi criada
if ! docker images | grep -q "recommender-agent"; then
    echo "❌ Erro: Imagem Docker não foi criada"
    exit 1
fi

echo "✅ Imagem Docker criada com sucesso"

# Parar container existente se estiver rodando
if docker ps | grep -q "recommender-agent"; then
    echo "🛑 Parando container existente..."
    docker stop recommender-agent || true
fi

# Remover container existente
if docker ps -a | grep -q "recommender-agent"; then
    echo "🗑️ Removendo container antigo..."
    docker rm recommender-agent || true
fi

# Executar novo container
echo "🚀 Iniciando novo container..."
docker run -d \
    --name recommender-agent \
    --network host \
    -p 5001:5001 \
    -e HOST=0.0.0.0 \
    -e PORT=5001 \
    -e DEBUG=False \
    recommender-agent:latest

# Aguardar inicialização
echo "⏳ Aguardando inicialização do serviço..."
sleep 5

# Verificar se o serviço está rodando
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ RecommenderAgent está rodando e saudável!"
    echo "🌐 Acesse: http://localhost:5001"
    echo "🏥 Health check: http://localhost:5001/health"
    echo "📊 Endpoint principal: http://localhost:5001/rank"
    
    # Mostrar informações do container
    echo "📦 Container info:"
    docker ps | grep recommender-agent
else
    echo "❌ Erro: Serviço não está respondendo"
    echo "📋 Logs do container:"
    docker logs recommender-agent
    exit 1
fi

echo "🎉 Deploy do RecommenderAgent concluído com sucesso!"
#!/bin/bash

# Script para build e deploy do Sustainable Shopping Advisor

set -e

echo "🌱 Sustainable Shopping Advisor - Build & Deploy Script"
echo "======================================================"

# Configurações
PROJECT_NAME="sustainable-advisor"
IMAGE_NAME="sustainable-advisor:latest"
NAMESPACE="default"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar dependências
check_dependencies() {
    print_status "Verificando dependências..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker não encontrado. Por favor, instale o Docker."
        exit 1
    fi
    
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl não encontrado. Por favor, instale o kubectl."
        exit 1
    fi
    
    print_success "Todas as dependências encontradas"
}

# Função para fazer build da imagem Docker
build_image() {
    print_status "Fazendo build da imagem Docker..."
    
    if docker build -t $IMAGE_NAME .; then
        print_success "Imagem Docker criada: $IMAGE_NAME"
    else
        print_error "Falha ao criar imagem Docker"
        exit 1
    fi
}

# Função para verificar se o cluster Kubernetes está acessível
check_k8s_cluster() {
    print_status "Verificando conectividade com cluster Kubernetes..."
    
    if kubectl cluster-info &> /dev/null; then
        print_success "Cluster Kubernetes acessível"
        kubectl get nodes
    else
        print_error "Não foi possível conectar ao cluster Kubernetes"
        exit 1
    fi
}

# Função para fazer deploy no Kubernetes
deploy_to_k8s() {
    print_status "Fazendo deploy no Kubernetes..."
    
    # Aplicar manifests
    if kubectl apply -f k8s-manifests.yaml; then
        print_success "Manifests aplicados com sucesso"
    else
        print_error "Falha ao aplicar manifests"
        exit 1
    fi
    
    # Aguardar deployment estar pronto
    print_status "Aguardando deployment ficar ready..."
    kubectl rollout status deployment/sustainable-advisor --timeout=300s
    
    print_success "Deployment concluído!"
}

# Função para verificar status do deployment
check_deployment_status() {
    print_status "Verificando status do deployment..."
    
    echo ""
    echo "=== Pods ==="
    kubectl get pods -l app=sustainable-advisor
    
    echo ""
    echo "=== Services ==="
    kubectl get svc sustainable-advisor
    
    echo ""
    echo "=== Health Check ==="
    POD_NAME=$(kubectl get pods -l app=sustainable-advisor -o jsonpath="{.items[0].metadata.name}")
    if [ -n "$POD_NAME" ]; then
        kubectl exec $POD_NAME -- curl -s http://localhost:5002/health | python3 -m json.tool || echo "Health check failed"
    fi
}

# Função para fazer port-forward para testes locais
setup_port_forward() {
    print_status "Configurando port-forward para testes locais..."
    print_warning "Execute em outro terminal para testar:"
    echo ""
    echo "kubectl port-forward svc/sustainable-advisor 5002:80"
    echo ""
    echo "Então acesse: http://localhost:5002"
    echo ""
}

# Função para fazer cleanup
cleanup() {
    print_status "Fazendo cleanup..."
    kubectl delete -f k8s-manifests.yaml --ignore-not-found=true
    print_success "Cleanup concluído"
}

# Menu principal
case "${1:-deploy}" in
    "build")
        check_dependencies
        build_image
        ;;
    "deploy")
        check_dependencies
        build_image
        check_k8s_cluster
        deploy_to_k8s
        check_deployment_status
        setup_port_forward
        ;;
    "status")
        check_deployment_status
        ;;
    "cleanup")
        cleanup
        ;;
    "help")
        echo "Uso: $0 [comando]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  build    - Fazer build apenas da imagem Docker"
        echo "  deploy   - Build e deploy completo (padrão)"
        echo "  status   - Verificar status do deployment"
        echo "  cleanup  - Remover todos os recursos do cluster"
        echo "  help     - Mostrar esta ajuda"
        ;;
    *)
        print_error "Comando inválido: $1"
        print_status "Use '$0 help' para ver comandos disponíveis"
        exit 1
        ;;
esac
#!/usr/bin/env python3
"""
Cliente de demonstração para testar a API do Sustainable Shopping Advisor
"""

import requests
import json
import time
from typing import Dict, Any

class SustainableAdvisorAPIClient:
    def __init__(self, base_url: str = "http://localhost:5002"):
        self.base_url = base_url.rstrip('/')
        
    def test_health(self) -> Dict[str, Any]:
        """Testa endpoint de health check"""
        print("🔍 Testando health check...")
        response = requests.get(f"{self.base_url}/health")
        return self._handle_response(response)
    
    def get_recommendations(self, user_preferences: Dict = None) -> Dict[str, Any]:
        """Obtém recomendações sustentáveis"""
        print("🌱 Obtendo recomendações sustentáveis...")
        
        if user_preferences:
            response = requests.post(
                f"{self.base_url}/recommendations",
                json={"user_preferences": user_preferences}
            )
        else:
            response = requests.get(f"{self.base_url}/recommendations")
            
        return self._handle_response(response)
    
    def get_sustainable_products(self) -> Dict[str, Any]:
        """Obtém apenas produtos sustentáveis (sem ranking)"""
        print("📦 Obtendo produtos sustentáveis...")
        response = requests.get(f"{self.base_url}/products/sustainable")
        return self._handle_response(response)
    
    def explain_product(self, product_id: str) -> Dict[str, Any]:
        """Obtém explicação detalhada de um produto"""
        print(f"💡 Explicando produto {product_id}...")
        response = requests.get(f"{self.base_url}/product/{product_id}/explanation")
        return self._handle_response(response)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas de sustentabilidade"""
        print("📊 Obtendo estatísticas...")
        response = requests.get(f"{self.base_url}/stats")
        return self._handle_response(response)
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Obtém configuração do agente"""
        print("⚙️ Obtendo configuração do agente...")
        response = requests.get(f"{self.base_url}/agent/config")
        return self._handle_response(response)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Processa resposta da API"""
        try:
            data = response.json()
            if response.status_code == 200:
                print(f"✅ Sucesso! Status: {response.status_code}")
                return data
            else:
                print(f"⚠️ Aviso! Status: {response.status_code}")
                return data
        except Exception as e:
            print(f"❌ Erro ao processar resposta: {e}")
            return {"error": str(e), "status_code": response.status_code}

def main():
    """Demonstração completa da API"""
    print("🌱 === SUSTAINABLE SHOPPING ADVISOR - DEMO ===")
    print("=" * 60)
    
    client = SustainableAdvisorAPIClient()
    
    # 1. Health Check
    print("\n1️⃣ HEALTH CHECK")
    print("-" * 30)
    health = client.test_health()
    print(json.dumps(health, indent=2, ensure_ascii=False))
    
    # 2. Recomendações Gerais
    print("\n2️⃣ RECOMENDAÇÕES GERAIS")
    print("-" * 30)
    recommendations = client.get_recommendations()
    if recommendations.get("status") == "success":
        total = recommendations.get("total_recommendations", 0)
        processing_time = recommendations.get("processing_time_seconds", 0)
        print(f"📊 Total de recomendações: {total}")
        print(f"⏱️ Tempo de processamento: {processing_time:.2f}s")
        
        for i, product in enumerate(recommendations.get("recommendations", [])[:3], 1):
            score = product.get("sustainability_analysis", {}).get("sustainability_score", 0)
            discount = product.get("discount", 0)
            print(f"  {i}. {product.get('name')} (Score: {score}/100, Desconto: {discount}%)")
    
    # 3. Recomendações com Preferências
    print("\n3️⃣ RECOMENDAÇÕES COM PREFERÊNCIAS")
    print("-" * 30)
    preferences = {"category": "kitchen", "budget": 50}
    kitchen_recs = client.get_recommendations(preferences)
    if kitchen_recs.get("status") == "success":
        kitchen_products = kitchen_recs.get("recommendations", [])
        kitchen_count = len([p for p in kitchen_products if "kitchen" in p.get("categories", [])])
        print(f"🍽️ Produtos de cozinha encontrados: {kitchen_count}")
    
    # 4. Explicação de Produto
    print("\n4️⃣ EXPLICAÇÃO DE PRODUTO ESPECÍFICO")
    print("-" * 30)
    if recommendations.get("recommendations"):
        first_product = recommendations["recommendations"][0]
        product_id = first_product.get("id")
        explanation = client.explain_product(product_id)
        if explanation.get("status") == "success":
            print(f"🔍 Produto: {explanation.get('product_name')}")
            print(f"📊 Score: {explanation.get('sustainability_score')}/100")
            print("💡 Explicação:")
            print(explanation.get("explanation", "").split("🔍 **Por que este produto é sustentável:**")[0])
    
    # 5. Estatísticas
    print("\n5️⃣ ESTATÍSTICAS DE SUSTENTABILIDADE")
    print("-" * 30)
    stats = client.get_stats()
    if stats.get("status") == "success":
        stats_data = stats.get("stats", {})
        print(f"📈 Taxa de sustentabilidade: {stats_data.get('sustainability_rate', 0)}%")
        print(f"📊 Score médio: {stats_data.get('average_sustainability_score', 0)}/100")
        print(f"🏷️ Top eco-tags: {[tag['tag'] for tag in stats_data.get('top_eco_tags', [])[:3]]}")
        
        carbon_dist = stats_data.get('carbon_score_distribution', {})
        print("💨 Distribuição de pegada de carbono:")
        print(f"  • Excelente (< 30): {carbon_dist.get('excellent', 0)} produtos")
        print(f"  • Bom (30-49): {carbon_dist.get('good', 0)} produtos")
        print(f"  • Regular (50-69): {carbon_dist.get('fair', 0)} produtos")
        print(f"  • Ruim (≥ 70): {carbon_dist.get('poor', 0)} produtos")
    
    # 6. Configuração do Agente
    print("\n6️⃣ CONFIGURAÇÃO DO AGENTE")
    print("-" * 30)
    config = client.get_agent_config()
    if config.get("status") == "success":
        agent_config = config.get("agent_config", {})
        rules = agent_config.get("sustainability_rules", {})
        print(f"🎯 Threshold de sustentabilidade: {rules.get('sustainability_score_threshold', 0)}")
        print(f"🌱 Threshold de carbono: {rules.get('carbon_score_threshold', 0)}")
        print(f"🔗 URL MCP: {agent_config.get('mcp_client_url', 'N/A')}")
        print(f"🤝 URL A2A: {agent_config.get('a2a_client_url', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("🌱 O Sustainable Shopping Advisor está funcionando perfeitamente!")
    print("🚀 Pronto para o hackathon!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
# src/sustainable-advisor/api.py
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import logging
import json
from datetime import datetime
from typing import Dict, Any, List
import os

from agent import SustainableAdvisorAgent

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar Flask app
app = Flask(__name__)
CORS(app)  # Permitir requests do frontend da Boutique

# Inicializar o agente principal
try:
    advisor_agent = SustainableAdvisorAgent()
    logger.info("✅ SustainableAdvisorAgent inicializado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao inicializar SustainableAdvisorAgent: {e}")
    advisor_agent = None

@app.route('/', methods=['GET'])
def home():
    """Página inicial da API com documentação"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌱 Sustainable Shopping Advisor API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2e8b57; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #2e8b57; }
            .method { background: #e7f3ff; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
            pre { background: #f1f1f1; padding: 10px; overflow-x: auto; }
            .status { color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Sustainable Shopping Advisor API</h1>
            <p>API inteligente para recomendações de produtos sustentáveis na Online Boutique</p>
            
            <div class="status">
                Status: {{ status }} | Agente: {{ agent_status }}
            </div>
            
            <h2>📋 Endpoints Disponíveis</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/health</strong>
                <p>Verificação de saúde da API e componentes</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET/POST</span> <strong>/recommendations</strong>
                <p>Obter recomendações de produtos sustentáveis rankeados</p>
                <pre>POST Body (opcional): {"user_preferences": {"category": "kitchen", "budget": 100}}</pre>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/product/&lt;id&gt;/explanation</strong>
                <p>Explicação detalhada sobre por que um produto é sustentável</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/stats</strong>
                <p>Estatísticas gerais de sustentabilidade do catálogo</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/products/sustainable</strong>
                <p>Lists all sustainable products without RecommenderAgent ranking</p>
            </div>
            
            <h2>🔗 Architecture</h2>
            <p>
                <strong>SustainableAdvisorAgent</strong> → MCP → Online Boutique Catalog<br>
                <strong>SustainableAdvisorAgent</strong> → A2A → RecommenderAgent → Final Ranking
            </p>
            
            <h2>📊 Usage Example</h2>
            <pre>
curl -X GET "{{ base_url }}/recommendations"
curl -X POST "{{ base_url }}/recommendations" -H "Content-Type: application/json" -d '{"user_preferences": {"category": "kitchen"}}'
curl -X GET "{{ base_url }}/stats"
            </pre>
        </div>
    </body>
    </html>
    """
    
    status = "🟢 Operacional" if advisor_agent else "🔴 Erro"
    agent_status = "✅ Ativo" if advisor_agent else "❌ Falha na inicialização"
    
    return render_template_string(
        html_template, 
        status=status,
        agent_status=agent_status,
        base_url=request.base_url.rstrip('/')
    )

@app.route('/health', methods=['GET'])
def health_check():
    """Health check para Kubernetes e monitoramento"""
    health_data = {
        "status": "healthy",
        "service": "sustainable-shopping-advisor",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    # Verificar componentes
    try:
        # Verificar SustainableAdvisorAgent
        if advisor_agent:
            health_data["components"]["sustainable_advisor_agent"] = "healthy"
            
            # Verificar A2A Client
            a2a_health = advisor_agent.a2a_client.health_check()
            health_data["components"]["a2a_client"] = a2a_health["status"]
            health_data["components"]["recommender_agent"] = a2a_health["status"]
            
            # Verificar MCP Client  
            try:
                products = advisor_agent.mcp_client.get_products()
                health_data["components"]["mcp_client"] = "healthy"
                health_data["components"]["product_catalog"] = "healthy" if products else "warning"
            except Exception as e:
                health_data["components"]["mcp_client"] = "unhealthy"
                health_data["components"]["product_catalog"] = "unhealthy"
        else:
            health_data["status"] = "unhealthy"
            health_data["components"]["sustainable_advisor_agent"] = "unhealthy"
            
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        health_data["status"] = "unhealthy"
        health_data["error"] = str(e)
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    return jsonify(health_data), status_code

@app.route('/recommendations', methods=['GET', 'POST'])
def get_sustainable_recommendations():
    """
    Endpoint principal para obter recomendações sustentáveis rankeadas
    """
    if not advisor_agent:
        return jsonify({
            "status": "error",
            "message": "SustainableAdvisorAgent não está disponível"
        }), 503
    
    try:
        # Obter preferências do usuário
        user_preferences = {}
        if request.method == 'POST':
            data = request.get_json() or {}
            user_preferences = data.get('user_preferences', {})
        elif request.args:
            user_preferences = dict(request.args)
        
        logger.info(f"📝 Solicitação de recomendações com preferências: {user_preferences}")
        
        # Obter recomendações rankeadas do agente
        start_time = datetime.now()
        recommendations = advisor_agent.get_ranked_products(user_preferences)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Preparar resposta
        response = {
            "status": "success",
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "processing_time_seconds": round(processing_time, 3),
            "sustainability_info": {
                "message": "Produtos selecionados com base em critérios de sustentabilidade",
                "criteria": [
                    "Low carbon footprint (carbon_score < 50)",
                    "Eco-friendly tags (sustainable, bamboo, local, etc.)",
                    "Renewable and biodegradable materials",
                    "Sustainable production practices"
                ],
                "ranking_process": [
                    "1. Sustainability analysis (SustainableAdvisorAgent)",
                    "2. Filtering by eco-friendly criteria",
                    "3. Ranking by promotions and preferences (RecommenderAgent)",
                    "4. Final score and explanations"
                ]
            },
            "request_metadata": {
                "user_preferences": user_preferences,
                "timestamp": datetime.now().isoformat(),
                "agent_version": "1.0.0"
            }
        }
        
        logger.info(f"✅ {len(recommendations)} recomendações geradas em {processing_time:.2f}s")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter recomendações: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/products/sustainable', methods=['GET'])
def get_sustainable_products():
    """
    Lists sustainable products without ranking (sustainability analysis only)
    """
    if not advisor_agent:
        return jsonify({
            "status": "error",
            "message": "SustainableAdvisorAgent is not available"
        }), 503
    
    try:
        user_preferences = dict(request.args) if request.args else {}
        
        # Get only sustainable products (without A2A ranking)
        sustainable_products = advisor_agent.get_sustainable_products(user_preferences)
        
        response = {
            "status": "success",
            "total_sustainable_products": len(sustainable_products),
            "products": sustainable_products,
            "sustainability_analysis_only": True,
            "note": "Products filtered only by sustainability criteria, without promotional ranking"
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Error getting sustainable products: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/product/<product_id>/explanation', methods=['GET'])
def explain_product_sustainability(product_id):
    """
    Explica em detalhes por que um produto específico é sustentável
    """
    if not advisor_agent:
        return jsonify({
            "status": "error",
            "message": "SustainableAdvisorAgent não está disponível"
        }), 503
    
    try:
        # Buscar produto específico nas recomendações
        recommendations = advisor_agent.get_sustainable_products()
        
        product = None
        for rec in recommendations:
            if rec.get('id') == product_id:
                product = rec
                break
        
        if not product:
            return jsonify({
                "status": "error",
                "message": f"Produto {product_id} não encontrado ou não é sustentável",
                "available_products": [p.get('id') for p in recommendations]
            }), 404
        
        # Gerar explicação detalhada
        explanation = advisor_agent.explain_recommendation(product)
        analysis = product.get("sustainability_analysis", {})
        
        response = {
            "status": "success",
            "product_id": product_id,
            "product_name": product.get('name'),
            "sustainability_score": analysis.get("sustainability_score", 0),
            "is_sustainable": analysis.get("is_sustainable", False),
            "explanation": explanation,
            "detailed_analysis": analysis,
            "eco_tags": product.get("eco_tags", []),
            "carbon_score": product.get("carbon_score"),
            "categories": product.get("categories", [])
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Erro ao explicar produto {product_id}: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def get_sustainability_stats():
    """
    Retorna estatísticas gerais de sustentabilidade do catálogo
    """
    if not advisor_agent:
        return jsonify({
            "status": "error",
            "message": "SustainableAdvisorAgent não está disponível"
        }), 503
    
    try:
        stats = advisor_agent.get_sustainability_stats()
        
        # Add extra information
        stats["api_info"] = {
            "endpoint": "/stats",
            "description": "Estatísticas de sustentabilidade do catálogo completo",
            "last_updated": datetime.now().isoformat()
        }
        
        return jsonify({
            "status": "success",
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/agent/config', methods=['GET'])
def get_agent_config():
    """
    Returns current agent configuration
    """
    if not advisor_agent:
        return jsonify({
            "status": "error",
            "message": "SustainableAdvisorAgent is not available"
        }), 503
    
    try:
        config = {
            "status": "success",
            "agent_config": {
                "sustainability_rules": advisor_agent.sustainability_rules,
                "mcp_client_url": advisor_agent.mcp_client.catalog_service_url,
                "a2a_client_url": advisor_agent.a2a_client.recommender_url,
                "version": "1.0.0"
            }
        }
        
        return jsonify(config)
        
    except Exception as e:
        logger.error(f"❌ Error getting configuration: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint não encontrado",
        "available_endpoints": [
            "/",
            "/health", 
            "/recommendations",
            "/products/sustainable",
            "/product/<id>/explanation",
            "/stats",
            "/agent/config"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno do servidor: {error}")
    return jsonify({
        "status": "error",
        "message": "Erro interno do servidor",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # Server configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Starting Sustainable Shopping Advisor API on {host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    
    if advisor_agent:
        logger.info("✅ Todos os componentes inicializados com sucesso")
    else:
        logger.warning("⚠️ API iniciando com componentes indisponíveis")
    
    app.run(host=host, port=port, debug=debug)
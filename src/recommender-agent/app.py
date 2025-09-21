#!/usr/bin/env python3
"""
RecommenderAgent - Agente especializado em ranking baseado em promoções e preferências
"""

from flask import Flask, request, jsonify
import logging
import json
import time
import random
from typing import List, Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class RecommenderAgent:
    """
    Agente especializado em ranking baseado em:
    1. Promoções ativas
    2. Preferências do usuário
    3. Padrões de comportamento
    4. Popularidade simulada
    """
    
    def __init__(self):
        # Promoções ativas (simuladas)
        self.promotions = {
            "0PUK6V6EV0": {"discount": 0.20, "reason": "Produto artesanal em destaque"},      # Candle Holder
            "9SIQT8TOJO": {"discount": 0.15, "reason": "Eco-friendly week special"},         # Bamboo Glass Jar
            "6E92ZMYYFZ": {"discount": 0.10, "reason": "Kitchen essentials discount"},       # Mug
            "L9ECAV7KIM": {"discount": 0.25, "reason": "Fashion summer sale"},              # Loafers
            "2ZYFJ3GM2N": {"discount": 0.12, "reason": "Beauty & care promotion"},          # Hairdryer
        }
        
        # Padrões de comportamento do usuário
        self.user_behavior_patterns = {
            "eco_conscious": {
                "eco_tags": ["sustainable", "bamboo", "organic", "recyclable", "local"],
                "boost_factor": 1.5,
                "description": "Usuários preocupados com sustentabilidade"
            },
            "home_decorator": {
                "categories": ["home", "decor", "kitchen"],
                "boost_factor": 1.3,
                "description": "Usuários interessados em decoração"
            },
            "budget_friendly": {
                "price_sensitive": True,
                "boost_factor": 1.4,
                "description": "Usuários sensíveis a preço e promoções"
            },
            "premium_buyer": {
                "quality_focused": True,
                "boost_factor": 1.2,
                "description": "Usuários que priorizam qualidade"
            }
        }
        
        # Tendências de mercado simuladas
        self.market_trends = {
            "sustainable_living": 1.6,
            "home_improvement": 1.3,
            "eco_kitchen": 1.4,
            "artisanal_products": 1.2
        }
        
        logger.info("🎯 RecommenderAgent inicializado")
        logger.info(f"📢 {len(self.promotions)} promoções ativas")
        logger.info(f"👥 {len(self.user_behavior_patterns)} padrões de comportamento configurados")

    def rank_products(self, products: List[Dict], user_preferences: Dict = None) -> List[Dict]:
        """
        Método principal para ranking de produtos
        """
        if not products:
            logger.warning("⚠️ Lista de produtos vazia recebida")
            return []
        
        logger.info(f"📊 Iniciando ranking de {len(products)} produtos")
        
        # Processar cada produto
        scored_products = []
        for product in products:
            enhanced_product = self._enhance_product_with_ranking(product, user_preferences)
            scored_products.append(enhanced_product)
        
        # Ordenar por ranking_score (decrescente)
        ranked_products = sorted(
            scored_products,
            key=lambda p: p.get("ranking_metadata", {}).get("final_ranking_score", 0),
            reverse=True
        )
        
        # Adicionar posições no ranking
        for i, product in enumerate(ranked_products, 1):
            product["ranking_metadata"]["rank_position"] = i
            product["ranking_metadata"]["is_top_recommendation"] = i <= 3
        
        logger.info(f"✅ Ranking concluído. Top produto: {ranked_products[0].get('name')}")
        logger.info(f"🏆 Score do líder: {ranked_products[0].get('ranking_metadata', {}).get('final_ranking_score', 0)}")
        
        return ranked_products

    def _enhance_product_with_ranking(self, product: Dict, user_preferences: Dict = None) -> Dict:
        """
        Adiciona informações de ranking a um produto
        """
        product_id = product.get("id")
        product_name = product.get("name", "Produto sem nome")
        
        # Score base (sustentabilidade)
        sustainability_score = product.get("sustainability_analysis", {}).get("sustainability_score", 0)
        
        # Calcular componentes do score
        promotion_score = self._calculate_promotion_score(product)
        preference_score = self._calculate_preference_score(product, user_preferences)
        popularity_score = self._calculate_popularity_score(product)
        trend_score = self._calculate_trend_score(product)
        
        # Score final ponderado
        final_score = (
            sustainability_score * 0.4 +      # 40% sustentabilidade
            promotion_score * 0.25 +          # 25% promoções
            preference_score * 0.20 +         # 20% preferências
            popularity_score * 0.10 +         # 10% popularidade
            trend_score * 0.05                # 5% tendências
        )
        
        # Aplicar desconto se há promoção
        discount_percent = 0
        promotion_reason = ""
        if product_id in self.promotions:
            promo = self.promotions[product_id]
            discount_percent = int(promo["discount"] * 100)
            promotion_reason = promo["reason"]
        
        # Metadados de ranking
        ranking_metadata = {
            "final_ranking_score": round(final_score, 2),
            "score_components": {
                "sustainability_score": sustainability_score,
                "promotion_score": promotion_score,
                "preference_score": preference_score,
                "popularity_score": popularity_score,
                "trend_score": trend_score
            },
            "has_promotion": product_id in self.promotions,
            "promotion_discount_percent": discount_percent,
            "promotion_reason": promotion_reason,
            "user_preference_match": self._check_user_preference_match(product, user_preferences),
            "recommendation_reasons": self._generate_recommendation_reasons(product, user_preferences),
            "ranking_algorithm": "multi_factor_weighted",
            "ranked_at": datetime.now().isoformat(),
            "agent_version": "1.0.0"
        }
        
        # Retornar produto com informações de ranking
        enhanced_product = {
            **product,
            "discount": discount_percent,  # Para compatibilidade
            "ranking_metadata": ranking_metadata
        }
        
        logger.debug(f"🔢 {product_name}: Score final {final_score:.2f} (Sus: {sustainability_score}, Promo: {promotion_score}, Pref: {preference_score})")
        
        return enhanced_product

    def _calculate_promotion_score(self, product: Dict) -> float:
        """
        Calcula score baseado em promoções ativas
        """
        product_id = product.get("id")
        
        if product_id not in self.promotions:
            return 0
        
        discount = self.promotions[product_id]["discount"]
        # Converter desconto em score (20% desconto = 20 pontos)
        promotion_score = discount * 100
        
        logger.debug(f"💰 {product.get('name')}: +{promotion_score} pontos por promoção")
        return promotion_score

    def _calculate_preference_score(self, product: Dict, user_preferences: Dict = None) -> float:
        """
        Calcula score baseado em preferências do usuário
        """
        if not user_preferences:
            return 0
        
        score = 0
        
        # Preferência por categorias
        preferred_categories = user_preferences.get("category", "").lower()
        if preferred_categories:
            product_categories = [cat.lower() for cat in product.get("categories", [])]
            if preferred_categories in product_categories:
                score += 30
                logger.debug(f"🎯 {product.get('name')}: +30 por categoria preferida ({preferred_categories})")
        
        # Preferência por sustentabilidade
        if user_preferences.get("eco_preference", False):
            eco_tags = product.get("eco_tags", [])
            if eco_tags:
                eco_bonus = len(eco_tags) * 10
                score += eco_bonus
                logger.debug(f"🌱 {product.get('name')}: +{eco_bonus} por eco-tags")
        
        # Sensibilidade a orçamento
        budget = user_preferences.get("budget", 0)
        if budget > 0:
            product_price = product.get("price_usd", {}).get("units", 0)
            if product_price <= budget:
                score += 20
                logger.debug(f"💵 {product.get('name')}: +20 por estar no orçamento")
        
        return score

    def _calculate_popularity_score(self, product: Dict) -> float:
        """
        Simula score de popularidade baseado em características
        """
        score = 0
        
        # Produtos com mais eco_tags são mais "populares"
        eco_tags_count = len(product.get("eco_tags", []))
        score += eco_tags_count * 8
        
        # Produtos com baixo carbon_score são mais procurados
        carbon_score = product.get("carbon_score", 100)
        if carbon_score < 50:
            carbon_bonus = (50 - carbon_score) * 0.8
            score += carbon_bonus
        
        # Categorias populares
        popular_categories = ["kitchen", "home", "decor"]
        product_categories = product.get("categories", [])
        for category in product_categories:
            if category in popular_categories:
                score += 15
                break
        
        # Fator de aleatoriedade para simular tendências dinâmicas
        trend_factor = random.uniform(5, 15)
        score += trend_factor
        
        return score

    def _calculate_trend_score(self, product: Dict) -> float:
        """
        Calcula score baseado em tendências de mercado
        """
        score = 0
        
        # Mapear produtos para tendências
        eco_tags = product.get("eco_tags", [])
        categories = product.get("categories", [])
        
        # Tendência sustentável
        if any(tag in ["sustainable", "bamboo", "organic"] for tag in eco_tags):
            score += self.market_trends["sustainable_living"] * 10
        
        # Tendência home improvement
        if any(cat in ["home", "decor"] for cat in categories):
            score += self.market_trends["home_improvement"] * 10
        
        # Tendência eco kitchen
        if "kitchen" in categories and eco_tags:
            score += self.market_trends["eco_kitchen"] * 10
        
        # Tendência artesanal
        if "handmade" in eco_tags:
            score += self.market_trends["artisanal_products"] * 10
        
        return score

    def _check_user_preference_match(self, product: Dict, user_preferences: Dict = None) -> Dict[str, Any]:
        """
        Verifica correspondência com preferências do usuário
        """
        if not user_preferences:
            return {"matches": False, "details": []}
        
        matches = []
        
        # Verificar categoria
        preferred_category = user_preferences.get("category", "").lower()
        if preferred_category:
            product_categories = [cat.lower() for cat in product.get("categories", [])]
            if preferred_category in product_categories:
                matches.append(f"Categoria preferida: {preferred_category}")
        
        # Verificar orçamento
        budget = user_preferences.get("budget", 0)
        if budget > 0:
            product_price = product.get("price_usd", {}).get("units", 0)
            if product_price <= budget:
                matches.append(f"Dentro do orçamento: ${product_price} ≤ ${budget}")
        
        # Verificar preferência eco
        if user_preferences.get("eco_preference") and product.get("eco_tags"):
            matches.append(f"Eco-friendly: {', '.join(product.get('eco_tags'))}")
        
        return {
            "matches": len(matches) > 0,
            "match_count": len(matches),
            "details": matches
        }

    def _generate_recommendation_reasons(self, product: Dict, user_preferences: Dict = None) -> List[str]:
        """
        Gera razões para a recomendação
        """
        reasons = []
        
        # Razão por sustentabilidade
        sustainability_score = product.get("sustainability_analysis", {}).get("sustainability_score", 0)
        if sustainability_score > 80:
            reasons.append(f"Excelente score de sustentabilidade ({sustainability_score}/100)")
        elif sustainability_score > 60:
            reasons.append(f"Bom score de sustentabilidade ({sustainability_score}/100)")
        
        # Razão por promoção
        product_id = product.get("id")
        if product_id in self.promotions:
            promo = self.promotions[product_id]
            discount_percent = int(promo["discount"] * 100)
            reasons.append(f"{discount_percent}% de desconto - {promo['reason']}")
        
        # Razão por eco-tags
        eco_tags = product.get("eco_tags", [])
        if eco_tags:
            reasons.append(f"Características sustentáveis: {', '.join(eco_tags)}")
        
        # Razão por baixa pegada de carbono
        carbon_score = product.get("carbon_score", 100)
        if carbon_score < 50:
            reasons.append(f"Baixa pegada de carbono (score: {carbon_score}/100)")
        
        # Razão por preferências do usuário
        if user_preferences:
            preference_match = self._check_user_preference_match(product, user_preferences)
            if preference_match["matches"]:
                reasons.append("Corresponde às suas preferências")
        
        # Razão padrão se não houver outras
        if not reasons:
            reasons.append("Produto recomendado com base na análise geral")
        
        return reasons

# Instanciar o agente
recommender = RecommenderAgent()

@app.route('/', methods=['GET'])
def home():
    """Página inicial do RecommenderAgent"""
    return jsonify({
        "service": "RecommenderAgent",
        "version": "1.0.0",
        "description": "Agente especializado em ranking de produtos baseado em promoções e preferências",
        "endpoints": {
            "POST /rank": "Rankear lista de produtos",
            "GET /health": "Health check",
            "GET /promotions": "Listar promoções ativas",
            "GET /trends": "Tendências de mercado",
            "GET /patterns": "Padrões de comportamento"
        },
        "active_promotions": len(recommender.promotions),
        "behavior_patterns": len(recommender.user_behavior_patterns),
        "status": "operational"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Verificar se o agente está funcionando
        test_product = {
            "id": "test",
            "name": "Test Product",
            "sustainability_analysis": {"sustainability_score": 50}
        }
        
        # Tentar fazer um ranking de teste
        test_result = recommender.rank_products([test_product])
        health_status = "healthy" if test_result else "degraded"
        
        return jsonify({
            "status": health_status,
            "service": "recommender-agent",
            "version": "1.0.0",
            "active_promotions": len(recommender.promotions),
            "behavior_patterns": len(recommender.user_behavior_patterns),
            "market_trends": len(recommender.market_trends),
            "last_check": datetime.now().isoformat(),
            "test_ranking": "passed" if test_result else "failed"
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "recommender-agent",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }), 503

@app.route('/rank', methods=['POST'])
def rank_products():
    """
    Endpoint principal para ranking de produtos
    Recebe lista de produtos e preferências do usuário
    Retorna produtos rankeados com metadados
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "JSON payload required",
                "expected_format": {
                    "products": [{"id": "...", "name": "...", "sustainability_analysis": {...}}],
                    "user_preferences": {"category": "...", "budget": 100, "eco_preference": True}
                }
            }), 400
        
        products = data.get("products", [])
        user_preferences = data.get("user_preferences", {})
        request_metadata = data.get("request_metadata", {})
        
        logger.info(f"📥 Recebida solicitação de ranking para {len(products)} produtos")
        if user_preferences:
            logger.info(f"👤 Preferências do usuário: {user_preferences}")
        
        if not products:
            return jsonify({"error": "No products provided"}), 400
        
        # Realizar ranking
        start_time = time.time()
        ranked_products = recommender.rank_products(products, user_preferences)
        processing_time = time.time() - start_time
        
        # Preparar resposta
        response = {
            "status": "success",
            "total_products": len(ranked_products),
            "processing_time_seconds": round(processing_time, 3),
            "ranking_summary": {
                "top_product": ranked_products[0].get("name") if ranked_products else None,
                "top_score": ranked_products[0].get("ranking_metadata", {}).get("final_ranking_score", 0) if ranked_products else 0,
                "products_with_promotions": len([p for p in ranked_products if p.get("ranking_metadata", {}).get("has_promotion")]),
                "avg_sustainability_score": round(sum(p.get("sustainability_analysis", {}).get("sustainability_score", 0) for p in ranked_products) / len(ranked_products), 2) if ranked_products else 0
            },
            "request_metadata": {
                **request_metadata,
                "processed_by": "RecommenderAgent",
                "processing_timestamp": datetime.now().isoformat(),
                "user_preferences_applied": bool(user_preferences)
            }
        }
        
        logger.info(f"📤 Ranking concluído em {processing_time:.3f}s. Top: {response['ranking_summary']['top_product']}")
        
        # Retornar apenas a lista rankeada (compatibilidade com A2A)
        return jsonify(ranked_products)
        
    except Exception as e:
        logger.error(f"❌ Erro no ranking: {e}")
        return jsonify({
            "error": "Internal ranking error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/promotions', methods=['GET'])
def get_active_promotions():
    """Retorna promoções ativas"""
    return jsonify({
        "status": "success",
        "active_promotions": recommender.promotions,
        "total_promotions": len(recommender.promotions),
        "promotion_summary": {
            "max_discount": max([p["discount"] for p in recommender.promotions.values()]) * 100,
            "min_discount": min([p["discount"] for p in recommender.promotions.values()]) * 100,
            "avg_discount": sum([p["discount"] for p in recommender.promotions.values()]) / len(recommender.promotions) * 100
        }
    })

@app.route('/trends', methods=['GET'])
def get_market_trends():
    """Retorna tendências de mercado"""
    return jsonify({
        "status": "success",
        "market_trends": recommender.market_trends,
        "trend_analysis": {
            "top_trend": max(recommender.market_trends.items(), key=lambda x: x[1]),
            "total_trends": len(recommender.market_trends)
        }
    })

@app.route('/patterns', methods=['GET'])
def get_user_patterns():
    """Retorna padrões de comportamento do usuário"""
    return jsonify({
        "status": "success",
        "behavior_patterns": recommender.user_behavior_patterns,
        "pattern_summary": {
            "total_patterns": len(recommender.user_behavior_patterns),
            "avg_boost_factor": sum([p["boost_factor"] for p in recommender.user_behavior_patterns.values()]) / len(recommender.user_behavior_patterns)
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": ["/", "/health", "/rank", "/promotions", "/trends", "/patterns"],
        "service": "RecommenderAgent"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {error}")
    return jsonify({
        "error": "Internal server error",
        "service": "RecommenderAgent",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    import os
    
    # Configurações do servidor
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Iniciando RecommenderAgent em {host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"📢 {len(recommender.promotions)} promoções configuradas")
    logger.info(f"👥 {len(recommender.user_behavior_patterns)} padrões de comportamento ativos")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor: {e}")
        raise
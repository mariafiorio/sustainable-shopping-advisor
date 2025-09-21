# src/sustainable-advisor/agent.py
import json
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from mcp_client import MCPClient
from a2a_client import A2AClient

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google AI integration
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logger.warning("Google AI not available - using fallback mode")

class SustainableAdvisorAgent:
    """
    Agente Inteligente de Sustentabilidade para Online Boutique
    
    Responsabilidades:
    1. Analisar produtos do catálogo usando critérios de sustentabilidade
    2. Filtrar produtos sustentáveis usando regras configuráveis
    3. Comunicar com RecommenderAgent via A2A para ranking final
    4. Fornecer explicações detalhadas sobre recomendações
    """
    
    def __init__(self):
        self.mcp_client = MCPClient()
        self.a2a_client = A2AClient()
        self.sustainability_rules = self._load_sustainability_rules()
        
        # Initialize Google AI if available
        self.google_ai_model = None
        self._init_google_ai()
        
        logger.info("🌱 SustainableAdvisorAgent inicializado")

    def _init_google_ai(self):
        """Initialize Google AI with API key from environment"""
        if GOOGLE_AI_AVAILABLE:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.google_ai_model = genai.GenerativeModel('gemini-1.5-flash')
                    logger.info("✅ Google AI configurado com sucesso")
                except Exception as e:
                    logger.error(f"❌ Erro ao configurar Google AI: {e}")
                    self.google_ai_model = None
            else:
                logger.warning("⚠️ GOOGLE_API_KEY não encontrada - usando modo fallback")
        else:
            logger.warning("⚠️ Google AI não disponível - usando modo fallback")

    def _load_sustainability_rules(self) -> Dict[str, Any]:
        """
        Define regras de sustentabilidade configuráveis
        """
        return {
            "carbon_score_threshold": 50,  # Produtos com score < 50 são sustentáveis
            "sustainability_score_threshold": 60,  # Score mínimo para ser recomendado
            
            "eco_categories": {
                "sustainable": {
                    "weight": 1.0, 
                    "reason": "Certificado como produto sustentável"
                },
                "bamboo": {
                    "weight": 0.9, 
                    "reason": "Material renovável e biodegradável"
                },
                "handmade": {
                    "weight": 0.9, 
                    "reason": "Produção artesanal reduz pegada industrial"
                },
                "local": {
                    "weight": 0.8, 
                    "reason": "Produção local reduz emissões de transporte"
                },
                "organic": {
                    "weight": 0.8, 
                    "reason": "Produção sem químicos nocivos ao meio ambiente"
                },
                "fair-trade": {
                    "weight": 0.8, 
                    "reason": "Comércio justo e práticas éticas"
                },
                "recyclable": {
                    "weight": 0.7, 
                    "reason": "Pode ser reciclado ao fim da vida útil"
                },
                "renewable": {
                    "weight": 0.7, 
                    "reason": "Feito com materiais renováveis"
                }
            },
            
            "sustainable_keywords": [
                "bamboo", "organic", "eco", "green", "sustainable", 
                "recycled", "natural", "biodegradable", "renewable",
                "handmade", "artisan", "local", "fair-trade"
            ],
            
            "category_sustainability_bonus": {
                "kitchen": 0.1,  # Produtos de cozinha tendem a ser duráveis
                "home": 0.1,     # Produtos para casa são investimentos de longo prazo
                "decor": 0.05    # Decoração pode ser sustentável
            }
        }

    def analyze_product_sustainability(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa um produto individual e calcula seu score de sustentabilidade
        
        Args:
            product: Dicionário com dados do produto
            
        Returns:
            Análise completa de sustentabilidade do produto
        """
        sustainability_score = 0
        reasons = []
        product_id = product.get('id', 'unknown')
        product_name = product.get('name', 'Produto sem nome')
        
        # 1. Análise por eco_tags
        eco_tags = product.get('eco_tags', [])
        for tag in eco_tags:
            if tag in self.sustainability_rules["eco_categories"]:
                rule = self.sustainability_rules["eco_categories"][tag]
                tag_score = rule["weight"] * 100
                sustainability_score += tag_score
                reasons.append({
                    "type": "eco_tag",
                    "tag": tag,
                    "score_added": tag_score,
                    "reason": f"✅ {tag.title()}: {rule['reason']}"
                })
        
        # 2. Análise por carbon_score
        carbon_score = product.get('carbon_score', 100)
        if carbon_score < self.sustainability_rules["carbon_score_threshold"]:
            carbon_bonus = (self.sustainability_rules["carbon_score_threshold"] - carbon_score) * 2
            sustainability_score += carbon_bonus
            reasons.append({
                "type": "carbon_score",
                "score_added": carbon_bonus,
                "reason": f"🌱 Baixa pegada de carbono: Score {carbon_score}/100"
            })
        
        # 3. Análise por palavras-chave no nome/descrição
        product_text = f"{product.get('name', '')} {product.get('description', '')}".lower()
        keywords_found = []
        for keyword in self.sustainability_rules["sustainable_keywords"]:
            if keyword in product_text:
                keywords_found.append(keyword)
        
        if keywords_found:
            keyword_bonus = len(keywords_found) * 15  # 15 pontos por palavra-chave
            sustainability_score += keyword_bonus
            reasons.append({
                "type": "keywords",
                "keywords": keywords_found,
                "score_added": keyword_bonus,
                "reason": f"🔍 Palavras-chave sustentáveis encontradas: {', '.join(keywords_found)}"
            })
        
        # 4. Bônus por categoria
        categories = product.get('categories', [])
        for category in categories:
            if category in self.sustainability_rules["category_sustainability_bonus"]:
                category_bonus = self.sustainability_rules["category_sustainability_bonus"][category] * 100
                sustainability_score += category_bonus
                reasons.append({
                    "type": "category_bonus",
                    "category": category,
                    "score_added": category_bonus,
                    "reason": f"🏷️ Categoria sustentável: {category}"
                })
        
        # Normaliza score (máximo 100)
        sustainability_score = min(sustainability_score, 100)
        is_sustainable = sustainability_score >= self.sustainability_rules["sustainability_score_threshold"]
        
        analysis = {
            "product_id": product_id,
            "product_name": product_name,
            "sustainability_score": round(sustainability_score, 2),
            "is_sustainable": is_sustainable,
            "carbon_score": carbon_score,
            "eco_tags": eco_tags,
            "categories": categories,
            "analysis_details": reasons,
            "analyzed_at": datetime.now().isoformat()
        }
        
        logger.debug(f"Produto {product_name}: Score {sustainability_score}/100 ({'✅' if is_sustainable else '❌'})")
        return analysis

    def get_sustainable_products(self, user_preferences: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Obtém e filtra produtos sustentáveis do catálogo
        
        Args:
            user_preferences: Preferências do usuário (opcional)
            
        Returns:
            Lista de produtos sustentáveis com análise completa
        """
        logger.info("🌱 Iniciando análise de sustentabilidade do catálogo")
        
        # 1. Busca produtos via MCP
        logger.info("📦 Buscando produtos do catálogo via MCP...")
        all_products = self.mcp_client.get_products()
        logger.info(f"✅ {len(all_products)} produtos encontrados no catálogo")
        
        if not all_products:
            logger.warning("⚠️ Nenhum produto encontrado no catálogo")
            return []
        
        # 2. Analisa sustentabilidade de cada produto
        logger.info("🔍 Analisando sustentabilidade dos produtos...")
        sustainable_products = []
        
        for product in all_products:
            analysis = self.analyze_product_sustainability(product)
            
            if analysis["is_sustainable"]:
                # Adiciona análise ao produto
                enhanced_product = {
                    **product,
                    "sustainability_analysis": analysis
                }
                sustainable_products.append(enhanced_product)
        
        logger.info(f"🌿 {len(sustainable_products)} produtos sustentáveis identificados")
        
        # 3. Ordena por score de sustentabilidade
        sustainable_products.sort(
            key=lambda p: p["sustainability_analysis"]["sustainability_score"], 
            reverse=True
        )
        
        return sustainable_products

    def get_ranked_products(self, user_preferences: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Obtém produtos sustentáveis e envia para RecommenderAgent para ranking final
        
        Args:
            user_preferences: Preferências do usuário
            
        Returns:
            Lista de produtos rankeados pelo RecommenderAgent
        """
        logger.info("🎯 Iniciando processo de recomendação sustentável")
        
        # 1. Obter produtos sustentáveis
        sustainable_products = self.get_sustainable_products(user_preferences)
        
        if not sustainable_products:
            logger.warning("⚠️ Nenhum produto sustentável encontrado")
            return []
        
        # 2. Enviar para RecommenderAgent via A2A
        logger.info("🤝 Enviando produtos para RecommenderAgent via A2A...")
        ranked_products = self.a2a_client.send_products_for_ranking(
            sustainable_products, 
            user_preferences
        )
        
        logger.info(f"🎯 {len(ranked_products)} recomendações finais recebidas")
        return ranked_products

    def explain_recommendation(self, product: Dict[str, Any]) -> str:
        """
        Gera explicação detalhada sobre por que um produto é recomendado
        
        Args:
            product: Produto com análise de sustentabilidade
            
        Returns:
            Explicação em linguagem natural
        """
        analysis = product.get("sustainability_analysis", {})
        
        if not analysis:
            return "❌ Análise de sustentabilidade não disponível para este produto."
        
        product_name = analysis.get("product_name", "Produto")
        score = analysis.get("sustainability_score", 0)
        details = analysis.get("analysis_details", [])
        
        explanation = f"🌱 **{product_name}**\n"
        explanation += f"📊 **Score de Sustentabilidade: {score}/100**\n\n"
        explanation += "🔍 **Por que este produto é sustentável:**\n\n"
        
        for detail in details:
            explanation += f"• {detail['reason']}\n"
        
        if analysis.get("carbon_score"):
            explanation += f"\n💨 **Pegada de Carbono:** {analysis.get('carbon_score')}/100 "
            explanation += "(quanto menor, melhor)\n"
        
        if analysis.get("eco_tags"):
            explanation += f"\n🏷️ **Tags Ecológicas:** {', '.join(analysis.get('eco_tags'))}\n"
        
        explanation += f"\n📅 **Análise realizada em:** {analysis.get('analyzed_at', 'N/A')}"
        
        return explanation

    def get_sustainability_stats(self) -> Dict[str, Any]:
        """
        Calcula estatísticas gerais de sustentabilidade do catálogo
        
        Returns:
            Estatísticas de sustentabilidade
        """
        logger.info("📊 Calculando estatísticas de sustentabilidade")
        
        sustainable_products = self.get_sustainable_products()
        
        if not sustainable_products:
            return {
                "total_sustainable_products": 0,
                "total_products_analyzed": 0,
                "sustainability_rate": 0,
                "average_sustainability_score": 0,
                "top_eco_tags": [],
                "carbon_score_distribution": {}
            }
        
        # Calcular estatísticas
        all_products = self.mcp_client.get_products()
        total_analyzed = len(all_products)
        total_sustainable = len(sustainable_products)
        sustainability_rate = (total_sustainable / total_analyzed * 100) if total_analyzed > 0 else 0
        
        # Score médio
        scores = [p["sustainability_analysis"]["sustainability_score"] for p in sustainable_products]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Tags mais comuns
        all_tags = []
        for product in sustainable_products:
            all_tags.extend(product.get("eco_tags", []))
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Distribuição de carbon_score
        carbon_scores = [p.get("carbon_score", 100) for p in sustainable_products]
        carbon_distribution = {
            "excellent": len([s for s in carbon_scores if s < 30]),    # < 30
            "good": len([s for s in carbon_scores if 30 <= s < 50]),   # 30-49
            "fair": len([s for s in carbon_scores if 50 <= s < 70]),   # 50-69
            "poor": len([s for s in carbon_scores if s >= 70])         # >= 70
        }
        
        stats = {
            "total_sustainable_products": total_sustainable,
            "total_products_analyzed": total_analyzed,
            "sustainability_rate": round(sustainability_rate, 2),
            "average_sustainability_score": round(avg_score, 2),
            "top_eco_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
            "carbon_score_distribution": carbon_distribution,
            "generated_at": datetime.now().isoformat()
        }
        
        logger.info(f"📊 Estatísticas: {total_sustainable}/{total_analyzed} produtos sustentáveis ({sustainability_rate:.1f}%)")
        return stats


# Classe de compatibilidade para manter interface existente
class SustainableAdvisorAgentLegacy:
    """Classe legada para compatibilidade com implementação anterior"""
    
    def __init__(self, **kwargs):
        self.agent = SustainableAdvisorAgent()
        logger.info("🔄 Usando SustainableAdvisorAgent via interface legada")

    def get_sustainable_products(self):
        """Método legado"""
        return self.agent.get_sustainable_products()

    def get_ranked_products(self):
        """Método legado"""
        return self.agent.get_ranked_products()


# Exemplo de execução
if __name__ == "__main__":
    logger.info("🚀 Iniciando demonstração do SustainableAdvisorAgent")
    
    # Criar agente
    agent = SustainableAdvisorAgent()
    
    # Obter recomendações rankeadas
    ranked_products = agent.get_ranked_products()
    
    print("\n🌱 Produtos Sustentáveis Rankeados:")
    print("=" * 50)
    
    for i, product in enumerate(ranked_products, 1):
        analysis = product.get("sustainability_analysis", {})
        score = analysis.get("sustainability_score", 0)
        discount = product.get("discount", 0)
        
        print(f"{i}. {product.get('name')} (Score: {score}/100, Desconto: {discount}%)")
        
        # Mostrar explicação para os 3 primeiros
        if i <= 3:
            explanation = agent.explain_recommendation(product)
            print(f"   💡 {explanation.split('Por que este produto é sustentável:')[0].strip()}")
            print()
    
    # Mostrar estatísticas
    print("\n📊 Estatísticas de Sustentabilidade:")
    print("=" * 50)
    stats = agent.get_sustainability_stats()
    print(f"• Total de produtos sustentáveis: {stats['total_sustainable_products']}")
    print(f"• Taxa de sustentabilidade: {stats['sustainability_rate']}%")
    print(f"• Score médio: {stats['average_sustainability_score']}/100")
    print(f"• Top eco-tags: {[tag['tag'] for tag in stats['top_eco_tags'][:3]]}")

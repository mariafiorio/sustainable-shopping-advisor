# src/sustainable-advisor/a2a_client.py
import requests
import json
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configurar logging
logger = logging.getLogger(__name__)

class A2AClient:
    """
    Cliente para comunicação Agent-to-Agent (A2A) com RecommenderAgent
    
    Responsabilidades:
    1. Enviar produtos sustentáveis para RecommenderAgent
    2. Receive ranking based on promotions and user preferences
    3. Implement robust fallbacks in case of failure
    4. Monitorar performance e logs da comunicação A2A
    """
    
    def __init__(self, recommender_url="http://localhost:5001/rank"):
        self.recommender_url = recommender_url
        self.timeout = 30  # segundos
        self.max_retries = 3
        self.retry_delay = 1  # segundos
        logger.info(f"🤝 A2AClient inicializado para {recommender_url}")

    def send_products_for_ranking(
        self, 
        products: List[Dict[str, Any]], 
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Envia produtos sustentáveis para o RecommenderAgent via A2A
        and receives refined ranking based on promotions and preferences
        
        Args:
            products: Lista de produtos sustentáveis com análise
            user_preferences: Preferências do usuário (opcional)
            
        Returns:
            Lista de produtos rankeados pelo RecommenderAgent
        """
        if not products:
            logger.warning("⚠️ Lista de produtos vazia - nada para ranker")
            return []
        
        logger.info(f"🔄 Iniciando comunicação A2A com {len(products)} produtos")
        
        # Preparar payload para A2A
        payload = self._prepare_a2a_payload(products, user_preferences)
        
        # Tentar comunicação com retries
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"🔄 Tentativa {attempt}/{self.max_retries} de comunicação A2A")
                response = self._send_request(payload, attempt)
                
                if response:
                    ranked_products = self._process_response(response, products)
                    logger.info(f"✅ Sucesso na comunicação A2A! {len(ranked_products)} produtos rankeados")
                    return ranked_products
                    
            except Exception as e:
                logger.error(f"❌ Erro na tentativa {attempt}: {e}")
                if attempt < self.max_retries:
                    logger.info(f"⏳ Aguardando {self.retry_delay}s antes da próxima tentativa...")
                    time.sleep(self.retry_delay)
                    self.retry_delay *= 2  # Exponential backoff
        
        # If all attempts failed, use fallback
        logger.warning("⚠️ All A2A communication attempts failed - using fallback")
        return self._fallback_ranking(products)

    def _prepare_a2a_payload(
        self, 
        products: List[Dict[str, Any]], 
        user_preferences: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prepara payload para comunicação A2A com RecommenderAgent
        """
        # Extract essential product information for sending
        simplified_products = []
        for product in products:
            simplified_product = {
                "id": product.get("id"),
                "name": product.get("name"),
                "description": product.get("description"),
                "categories": product.get("categories", []),
                "price_usd": product.get("priceUsd") or product.get("price_usd"),
                "sustainability_score": product.get("sustainability_analysis", {}).get("sustainability_score", 0),
                "eco_tags": product.get("eco_tags", []),
                "carbon_score": product.get("carbon_score", 100)
            }
            simplified_products.append(simplified_product)
        
        payload = {
            "products": simplified_products,
            "user_preferences": user_preferences or {},
            "request_metadata": {
                "agent_id": "sustainable_advisor_agent",
                "request_type": "sustainability_ranking",
                "timestamp": datetime.now().isoformat(),
                "total_products": len(products),
                "sustainability_context": {
                    "avg_sustainability_score": sum(
                        p.get("sustainability_analysis", {}).get("sustainability_score", 0) 
                        for p in products
                    ) / len(products) if products else 0,
                    "has_eco_tags": any(p.get("eco_tags") for p in products),
                    "carbon_scores_range": {
                        "min": min((p.get("carbon_score", 100) for p in products), default=100),
                        "max": max((p.get("carbon_score", 100) for p in products), default=100)
                    }
                }
            }
        }
        
        logger.debug(f"📋 Payload A2A preparado: {len(simplified_products)} produtos")
        return payload

    def _send_request(self, payload: Dict[str, Any], attempt: int) -> Optional[requests.Response]:
        """
        Envia requisição HTTP para RecommenderAgent
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "SustainableAdvisorAgent/1.0",
            "X-Request-ID": f"sustainable-advisor-{int(time.time())}-{attempt}",
            "X-Agent-Communication": "A2A"
        }
        
        try:
            logger.debug(f"🌐 Enviando requisição para {self.recommender_url}")
            response = requests.post(
                self.recommender_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            # Log da resposta
            logger.debug(f"📨 Resposta HTTP: {response.status_code}")
            
            if response.status_code == 200:
                return response
            else:
                logger.warning(f"⚠️ RecommenderAgent retornou status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout na comunicação A2A após {self.timeout}s")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"🔌 Erro de conexão com RecommenderAgent em {self.recommender_url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"🌐 Erro na requisição HTTP: {e}")
            return None

    def _process_response(
        self, 
        response: requests.Response, 
        original_products: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processa resposta do RecommenderAgent e reconstrói produtos completos
        """
        try:
            ranked_data = response.json()
            logger.debug(f"📥 Data received from RecommenderAgent: {type(ranked_data)}")
            
            # If the response is a simple list (RecommenderAgent fallback)
            if isinstance(ranked_data, list):
                logger.debug("📝 Processando resposta como lista simples")
                return self._reconstruct_products_from_simple_list(ranked_data, original_products)
            
            # Se a resposta tem estrutura mais complexa
            elif isinstance(ranked_data, dict):
                products_list = ranked_data.get("ranked_products", ranked_data.get("products", []))
                logger.debug(f"📝 Processando resposta estruturada com {len(products_list)} produtos")
                return self._reconstruct_products_from_simple_list(products_list, original_products)
            
            else:
                logger.warning(f"⚠️ Formato de resposta inesperado: {type(ranked_data)}")
                return self._fallback_ranking(original_products)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao decodificar JSON da resposta: {e}")
            logger.debug(f"📄 Resposta raw: {response.text[:500]}")
            return self._fallback_ranking(original_products)
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao processar resposta: {e}")
            return self._fallback_ranking(original_products)

    def _reconstruct_products_from_simple_list(
        self, 
        ranked_list: List[Dict[str, Any]], 
        original_products: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Reconstrói produtos completos a partir da lista rankeada simples
        """
        # Criar mapeamento de ID para produto original
        product_map = {p.get("id"): p for p in original_products}
        
        reconstructed_products = []
        for ranked_item in ranked_list:
            product_id = ranked_item.get("id")
            original_product = product_map.get(product_id)
            
            if original_product:
                # Mesclar dados originais com dados do ranking
                enhanced_product = {
                    **original_product,
                    **ranked_item,  # Sobrescreve com dados do ranking (como discount, rank_score, etc.)
                    "ranking_metadata": {
                        "ranked_by": "RecommenderAgent",
                        "ranking_timestamp": datetime.now().isoformat(),
                        "original_sustainability_score": original_product.get("sustainability_analysis", {}).get("sustainability_score", 0)
                    }
                }
                reconstructed_products.append(enhanced_product)
            else:
                logger.warning(f"⚠️ Produto {product_id} não encontrado no conjunto original")
        
        logger.info(f"🔧 Reconstruídos {len(reconstructed_products)} produtos completos")
        return reconstructed_products

    def _fallback_ranking(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranking fallback baseado apenas no sustainability_score quando A2A falha
        """
        logger.info("🔄 Executando ranking fallback baseado em sustainability_score")
        
        try:
            # Ordenar por sustainability_score
            fallback_products = sorted(
                products,
                key=lambda p: p.get("sustainability_analysis", {}).get("sustainability_score", 0),
                reverse=True
            )
            
            # Adicionar metadados de fallback
            for i, product in enumerate(fallback_products):
                product["ranking_metadata"] = {
                    "ranked_by": "SustainableAdvisorAgent_Fallback",
                    "ranking_timestamp": datetime.now().isoformat(),
                    "fallback_reason": "RecommenderAgent_communication_failed",
                    "fallback_rank": i + 1
                }
                
                # Simular alguns descontos baseados no score de sustentabilidade
                sustainability_score = product.get("sustainability_analysis", {}).get("sustainability_score", 0)
                if sustainability_score >= 80:
                    product["discount"] = 15  # 15% para produtos muito sustentáveis
                elif sustainability_score >= 60:
                    product["discount"] = 10  # 10% para produtos sustentáveis
                else:
                    product["discount"] = 5   # 5% desconto básico
            
            logger.info(f"✅ Ranking fallback concluído com {len(fallback_products)} produtos")
            return fallback_products
            
        except Exception as e:
            logger.error(f"❌ Erro crítico no ranking fallback: {e}")
            return products  # Retorna produtos sem modificação como último recurso

    def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde da comunicação com RecommenderAgent
        """
        try:
            # Tentar uma requisição simples de health check
            health_url = self.recommender_url.replace("/rank", "/health")
            response = requests.get(health_url, timeout=5)
            
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "recommender_url": self.recommender_url,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "recommender_url": self.recommender_url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

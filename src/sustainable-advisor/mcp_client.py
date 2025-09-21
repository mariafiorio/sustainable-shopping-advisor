# src/sustainable-advisor/mcp_client.py
import requests
import json
import os

class MCPClient:
    def __init__(self, catalog_service_url="http://34.66.235.59"):
        self.catalog_service_url = catalog_service_url
        # Path to local products data
        self.local_products_path = "../productcatalogservice/products.json"

    def get_products(self):
        """
        Consulta todos os produtos disponíveis na Boutique.
        Tenta diferentes estratégias para buscar produtos remotos.
        """
        # Estratégia 1: Tentar buscar através dos endpoints conhecidos
        products = self._fetch_from_remote_endpoints()
        if products:
            return self._add_sustainability_data(products)
        
        # Estratégia 2: Buscar produtos individuais usando IDs conhecidos
        products = self._fetch_individual_products()
        if products:
            return self._add_sustainability_data(products)
        
        # Fallback: Usar dados locais
        print("Todas as tentativas remotas falharam. Usando dados locais...")
        return self._get_local_products()

    def _fetch_from_remote_endpoints(self):
        """
        Tenta buscar produtos de diferentes endpoints possíveis.
        """
        endpoints_to_try = [
            f"{self.catalog_service_url}/api/products",
            f"{self.catalog_service_url}/products", 
            f"{self.catalog_service_url}/catalog",
            f"{self.catalog_service_url}/api/catalog"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                print(f"Tentando endpoint: {endpoint}")
                response = requests.get(endpoint, timeout=10)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        products = data.get('products', data) if isinstance(data, dict) else data
                        if products and isinstance(products, list) and len(products) > 0:
                            print(f"✓ Sucesso! Encontrados {len(products)} produtos em {endpoint}")
                            return products
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                print(f"  Erro: {e}")
                continue
        
        return []

    def _fetch_individual_products(self):
        """
        Busca produtos individuais usando IDs conhecidos do catálogo.
        """
        # IDs de produtos conhecidos do catálogo
        known_product_ids = [
            "OLJCESPC7Z",  # Sunglasses
            "66VCHSJNUP",  # Tank Top  
            "1YMWWN1N4O",  # Watch
            "L9ECAV7KIM",  # Loafers
            "2ZYFJ3GM2N",  # Hairdryer
            "0PUK6V6EV0",  # Candle Holder
            "LS4PSXUNUM",  # Salt & Pepper Shakers
            "9SIQT8TOJO",  # Bamboo Glass Jar
            "6E92ZMYYFZ"   # Mug
        ]
        
        products = []
        print("Tentando buscar produtos individuais...")
        
        for product_id in known_product_ids:
            try:
                endpoint = f"{self.catalog_service_url}/product-meta/{product_id}"
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    product = response.json()
                    products.append(product)
                    print(f"  ✓ {product.get('name', product_id)}")
            except Exception as e:
                print(f"  ✗ Erro ao buscar {product_id}: {e}")
                continue
        
        if products:
            print(f"✓ Sucesso! Coletados {len(products)} produtos via API individual")
            return products
        
        return []

    def _get_local_products(self):
        """
        Carrega produtos do arquivo JSON local.
        """
        try:
            # Caminho relativo ao diretório atual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            products_file = os.path.join(current_dir, self.local_products_path)
            
            with open(products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products = data.get('products', [])
                print(f"✓ Carregados {len(products)} produtos do arquivo local")
                return self._add_sustainability_data(products)
        except Exception as e:
            print(f"Erro ao carregar produtos locais: {e}")
            return []

    def _add_sustainability_data(self, products):
        """
        Adiciona dados de sustentabilidade aos produtos para demonstração.
        """
        sustainability_data = {
            "9SIQT8TOJO": {"eco_tags": ["sustainable", "bamboo"], "carbon_score": 25},  # Bamboo Glass Jar
            "0PUK6V6EV0": {"eco_tags": ["handmade", "local"], "carbon_score": 35},     # Candle Holder
            "6E92ZMYYFZ": {"eco_tags": ["recyclable"], "carbon_score": 45},            # Mug
            "L9ECAV7KIM": {"eco_tags": [], "carbon_score": 75},                        # Loafers
            "2ZYFJ3GM2N": {"eco_tags": [], "carbon_score": 85},                        # Hairdryer
            "1YMWWN1N4O": {"eco_tags": [], "carbon_score": 90},                        # Watch
        }
        
        for product in products:
            product_id = product.get('id')
            if product_id in sustainability_data:
                product.update(sustainability_data[product_id])
            else:
                # Produtos sem dados específicos recebem valores padrão
                product['eco_tags'] = []
                product['carbon_score'] = 60
        
        return products

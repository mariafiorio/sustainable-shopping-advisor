# src/adk/sustainable_advisor_adk.py
"""
SustainableAdvisor Agent using ADK Framework
Model-agnostic, modular, flexible agent for sustainability analysis
"""

import os
import logging
from typing import Dict, Any, List
from agent_base import BaseAgent, AgentCapability, AgentTool, GeminiModelProvider

logger = logging.getLogger(__name__)

class SustainableAdvisorADK(BaseAgent):
    """
    SustainableAdvisor using Agent Development Kit (ADK)
    
    Capabilities:
    - analyze_sustainability: Analyze products for sustainability metrics
    - get_recommendations: Get top sustainable product recommendations
    - calculate_eco_score: Calculate environmental impact score
    - ai_explanation: Generate AI-powered sustainability explanations
    
    Design: Modular, model-agnostic, deployment-agnostic
    """
    
    def __init__(self):
        # Initialize with ADK framework
        super().__init__(
            agent_id="sustainable-advisor-001",
            name="SustainableAdvisor",
            version="2.0.0-adk"
        )
        
        # Model provider setup (model-agnostic)
        self.model_provider = None
        self._setup_model_provider()
        
        # Agent configuration
        self.config = {
            "sustainability_threshold": 70,
            "recommendation_limit": 3,
            "eco_categories": {
                "bamboo": {"weight": 0.9, "bonus": 20},
                "organic": {"weight": 0.8, "bonus": 15},
                "recycled": {"weight": 0.8, "bonus": 15},
                "handmade": {"weight": 0.7, "bonus": 10},
                "local": {"weight": 0.7, "bonus": 10}
            }
        }
        
        self.logger.info("SustainableAdvisor ADK Agent ready")
    
    def _setup_model_provider(self):
        """Setup model provider (Gemini or fallback)"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            try:
                self.model_provider = GeminiModelProvider(api_key)
                self.logger.info("✅ Gemini model provider initialized")
            except Exception as e:
                self.logger.warning(f"⚠️ Gemini setup failed: {e}")
        else:
            self.logger.warning("⚠️ No API key found, using fallback mode")
    
    def _register_capabilities(self):
        """Register agent capabilities using ADK framework"""
        
        # Capability: Analyze Sustainability
        analyze_capability = AgentCapability(
            name="analyze_sustainability",
            description="Analyze products for sustainability metrics and environmental impact",
            handler=self._analyze_sustainability,
            input_schema={
                "products": "List[Dict] - Products to analyze",
                "criteria": "Optional[List[str]] - Sustainability criteria to evaluate"
            },
            output_schema={
                "analyzed_products": "List[Dict] - Products with sustainability analysis",
                "summary": "Dict - Analysis summary and statistics"
            },
            requirements=["product_data"]
        )
        self.register_capability(analyze_capability)
        
        # Capability: Get Recommendations
        recommendations_capability = AgentCapability(
            name="get_recommendations",
            description="Get top sustainable product recommendations",
            handler=self._get_recommendations,
            input_schema={
                "products": "List[Dict] - Products to rank",
                "limit": "Optional[int] - Number of recommendations (default: 3)"
            },
            output_schema={
                "recommendations": "List[Dict] - Top sustainable recommendations",
                "ranking_criteria": "Dict - Criteria used for ranking"
            },
            requirements=["analyzed_products"]
        )
        self.register_capability(recommendations_capability)
        
        # Capability: Calculate Eco Score
        eco_score_capability = AgentCapability(
            name="calculate_eco_score",
            description="Calculate environmental impact score for a product",
            handler=self._calculate_eco_score,
            input_schema={
                "product": "Dict - Product to evaluate"
            },
            output_schema={
                "eco_score": "int - Environmental score (0-100)",
                "factors": "Dict - Factors contributing to score",
                "grade": "str - Letter grade (A-F)"
            },
            requirements=["product_data"]
        )
        self.register_capability(eco_score_capability)
        
        # Capability: AI Explanation
        ai_explanation_capability = AgentCapability(
            name="ai_explanation",
            description="Generate AI-powered sustainability explanations",
            handler=self._ai_explanation,
            input_schema={
                "product": "Dict - Product to explain",
                "score": "int - Sustainability score"
            },
            output_schema={
                "explanation": "str - AI-generated explanation",
                "key_factors": "List[str] - Key sustainability factors"
            },
            requirements=["ai_model"]
        )
        self.register_capability(ai_explanation_capability)
    
    def _register_tools(self):
        """Register agent tools using ADK framework"""
        
        # Tool: Sustainability Calculator
        calculator_tool = AgentTool(
            name="sustainability_calculator",
            description="Calculate sustainability metrics based on product attributes",
            function=self._sustainability_calculator_tool,
            parameters={
                "product": "Dict - Product data",
                "criteria": "List[str] - Evaluation criteria"
            },
            model_agnostic=True
        )
        self.register_tool(calculator_tool)
        
        # Tool: Eco Category Analyzer
        category_tool = AgentTool(
            name="eco_category_analyzer",
            description="Analyze product categories for eco-friendliness",
            function=self._eco_category_analyzer_tool,
            parameters={
                "categories": "List[str] - Product categories",
                "description": "str - Product description"
            },
            model_agnostic=True
        )
        self.register_tool(category_tool)
        
        # Tool: AI Text Generator
        ai_tool = AgentTool(
            name="ai_text_generator",
            description="Generate explanatory text using AI models",
            function=self._ai_text_generator_tool,
            parameters={
                "prompt": "str - Generation prompt",
                "context": "Dict - Additional context"
            },
            model_agnostic=False  # Depends on model provider
        )
        self.register_tool(ai_tool)
    
    def _analyze_sustainability(self, parameters: Dict, context: Dict) -> Dict:
        """Analyze products for sustainability - ADK capability"""
        products = parameters.get('products', [])
        criteria = parameters.get('criteria', ['eco_friendly', 'carbon_footprint', 'materials'])
        
        analyzed_products = []
        total_score = 0
        sustainable_count = 0
        
        for product in products:
            # Calculate eco score using ADK tool
            eco_result = self.tools['sustainability_calculator'].function(
                product=product,
                criteria=criteria
            )
            
            # Analyze categories using ADK tool
            category_result = self.tools['eco_category_analyzer'].function(
                categories=product.get('categories', []),
                description=product.get('description', '')
            )
            
            # Combine results
            sustainability_score = eco_result['score']
            is_sustainable = sustainability_score >= self.config['sustainability_threshold']
            
            analyzed_product = {
                'product': product,
                'sustainability_score': sustainability_score,
                'eco_factors': eco_result['factors'],
                'category_analysis': category_result,
                'is_sustainable': is_sustainable,
                'grade': self._score_to_grade(sustainability_score),
                'recommendations': eco_result.get('recommendations', [])
            }
            
            analyzed_products.append(analyzed_product)
            total_score += sustainability_score
            
            if is_sustainable:
                sustainable_count += 1
        
        # Generate summary
        summary = {
            'total_products': len(products),
            'sustainable_products': sustainable_count,
            'average_score': round(total_score / len(products), 2) if products else 0,
            'sustainability_rate': round((sustainable_count / len(products)) * 100, 1) if products else 0,
            'criteria_used': criteria
        }
        
        return {
            'analyzed_products': analyzed_products,
            'summary': summary,
            'agent_version': self.version,
            'framework': 'adk'
        }
    
    def _get_recommendations(self, parameters: Dict, context: Dict) -> Dict:
        """Get top sustainable recommendations - ADK capability"""
        products = parameters.get('products', [])
        limit = parameters.get('limit', self.config['recommendation_limit'])
        
        # If products are not analyzed, analyze them first
        if products and 'sustainability_score' not in products[0]:
            analysis = self._analyze_sustainability({'products': products}, context)
            analyzed_products = analysis['analyzed_products']
        else:
            analyzed_products = products
        
        # Sort by sustainability score
        sorted_products = sorted(
            analyzed_products,
            key=lambda x: x.get('sustainability_score', 0),
            reverse=True
        )
        
        # Get top recommendations
        recommendations = sorted_products[:limit]
        
        # Add ranking metadata
        for i, rec in enumerate(recommendations):
            rec['ranking'] = {
                'position': i + 1,
                'score': rec.get('sustainability_score', 0),
                'percentage': round((rec.get('sustainability_score', 0) / 100) * 100, 1)
            }
        
        return {
            'recommendations': recommendations,
            'total_evaluated': len(analyzed_products),
            'ranking_criteria': {
                'primary': 'sustainability_score',
                'threshold': self.config['sustainability_threshold'],
                'framework': 'adk_based'
            },
            'agent_id': self.agent_id
        }
    
    def _calculate_eco_score(self, parameters: Dict, context: Dict) -> Dict:
        """Calculate eco score for single product - ADK capability"""
        product = parameters.get('product', {})
        
        # Use sustainability calculator tool
        result = self.tools['sustainability_calculator'].function(
            product=product,
            criteria=['materials', 'production', 'lifecycle']
        )
        
        eco_score = result['score']
        
        return {
            'eco_score': eco_score,
            'factors': result['factors'],
            'grade': self._score_to_grade(eco_score),
            'product_name': product.get('name', 'Unknown'),
            'calculated_by': 'adk_sustainability_calculator'
        }
    
    def _ai_explanation(self, parameters: Dict, context: Dict) -> Dict:
        """Generate AI explanation - ADK capability"""
        product = parameters.get('product', {})
        score = parameters.get('score', 0)
        
        if not self.model_provider:
            # Fallback explanation
            explanation = f"This product scores {score}/100 for sustainability based on eco-friendly features and materials."
            key_factors = ['materials', 'production_method', 'environmental_impact']
        else:
            # Use AI tool for generation
            ai_result = self.tools['ai_text_generator'].function(
                prompt=f"Explain why {product.get('name', 'this product')} has a sustainability score of {score}/100",
                context={'product': product, 'score': score}
            )
            explanation = ai_result['text']
            key_factors = ai_result.get('factors', [])
        
        return {
            'explanation': explanation,
            'key_factors': key_factors,
            'sustainability_score': score,
            'generated_by': 'adk_ai_explanation',
            'model_provider': self.model_provider.get_model_info() if self.model_provider else 'fallback'
        }
    
    # ADK Tools Implementation
    def _sustainability_calculator_tool(self, product: Dict, criteria: List[str]) -> Dict:
        """Sustainability calculator tool"""
        name = product.get('name', '').lower()
        description = product.get('description', '').lower()
        categories = product.get('categories', [])
        
        score = 50  # Base score
        factors = {'base_score': 50}
        recommendations = []
        
        # Eco-friendly keywords analysis
        eco_keywords = {
            'bamboo': 20,
            'organic': 15,
            'recycled': 15,
            'renewable': 12,
            'biodegradable': 12,
            'sustainable': 10,
            'eco': 8,
            'natural': 8,
            'handmade': 8,
            'local': 6
        }
        
        for keyword, bonus in eco_keywords.items():
            if keyword in name or keyword in description:
                score += bonus
                factors[f'{keyword}_bonus'] = bonus
        
        # Category analysis
        sustainable_categories = {
            'home': 5,
            'kitchen': 5,
            'garden': 8,
            'books': 10
        }
        
        for category in categories:
            if category.lower() in sustainable_categories:
                bonus = sustainable_categories[category.lower()]
                score += bonus
                factors[f'{category}_category'] = bonus
        
        # Ensure score is within bounds
        score = min(100, max(0, score))
        
        # Generate recommendations
        if score < 70:
            recommendations.append("Consider eco-friendly alternatives")
        if score < 50:
            recommendations.append("Look for recycled or renewable materials")
        
        return {
            'score': score,
            'factors': factors,
            'recommendations': recommendations
        }
    
    def _eco_category_analyzer_tool(self, categories: List[str], description: str) -> Dict:
        """Eco category analyzer tool"""
        eco_friendly_categories = ['home', 'garden', 'kitchen', 'books', 'handmade']
        
        category_scores = {}
        total_eco_score = 0
        
        for category in categories:
            if category.lower() in eco_friendly_categories:
                category_scores[category] = 'eco_friendly'
                total_eco_score += 1
            else:
                category_scores[category] = 'neutral'
        
        eco_percentage = (total_eco_score / len(categories)) * 100 if categories else 0
        
        return {
            'category_scores': category_scores,
            'eco_percentage': round(eco_percentage, 1),
            'eco_friendly_count': total_eco_score,
            'total_categories': len(categories)
        }
    
    def _ai_text_generator_tool(self, prompt: str, context: Dict) -> Dict:
        """AI text generator tool"""
        if not self.model_provider:
            return {
                'text': "AI explanation not available - using fallback mode",
                'factors': ['material_quality', 'production_method'],
                'model': 'fallback'
            }
        
        try:
            # Generate with model provider
            full_prompt = f"""
            {prompt}
            
            Context: {context.get('product', {}).get('description', '')}
            Score: {context.get('score', 'unknown')}
            
            Provide a concise explanation focusing on environmental benefits and sustainability factors.
            """
            
            generated_text = self.model_provider.generate_text(full_prompt)
            
            # Extract key factors (simple approach)
            factors = []
            factor_keywords = ['material', 'production', 'energy', 'waste', 'carbon', 'renewable']
            for keyword in factor_keywords:
                if keyword.lower() in generated_text.lower():
                    factors.append(keyword)
            
            return {
                'text': generated_text.strip(),
                'factors': factors,
                'model': self.model_provider.get_model_info()
            }
            
        except Exception as e:
            self.logger.error(f"AI generation failed: {e}")
            return {
                'text': f"Sustainability analysis indicates positive environmental impact with score {context.get('score', 'unknown')}/100",
                'factors': ['eco_friendly_materials'],
                'model': 'fallback_due_to_error'
            }
    
    def _score_to_grade(self, score: int) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
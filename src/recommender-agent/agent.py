# src/recommender-agent/agent.py

from google.adk.agents import Agent
from flask import Flask, request, jsonify

app = Flask(__name__)

class RecommenderAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RecommenderAgent",
            model="gemini-2.0-flash",  # Use sua chave Gemini
            description="Agente que rankeia produtos com base em promoções e preferências do usuário",
            instruction="You are a promotions consultant. Rank products received from SustainableAdvisorAgent.",
        )

    def rank_products(self, products):
        """
        Simple ranking example:
        - Prioritizes products with higher discounts
        - Can add filters based on user history or preferences
        """
        # Ordena produtos do maior para menor desconto
        ranked = sorted(products, key=lambda x: x.get("discount", 0), reverse=True)
        return ranked


# Inicializa o agente
root_agent = RecommenderAgent()

# API Flask para receber produtos via A2A
@app.route("/rank", methods=["POST"])
def rank_endpoint():
    products = request.json
    ranked_products = root_agent.rank_products(products)
    return jsonify(ranked_products)


if __name__ == "__main__":
    # Roda Flask na porta 5000 para comunicação A2A
    app.run(host="0.0.0.0", port=5001)

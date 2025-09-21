import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/rank", methods=["POST"])
def rank_products():
    products = request.json
    # Exemplo simples de ranking: prioriza produtos em promoção
    ranked = sorted(products, key=lambda x: x.get("discount", 0), reverse=True)
    return jsonify(ranked)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

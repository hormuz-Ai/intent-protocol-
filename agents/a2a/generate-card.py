from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

@app.route('/generate-card', methods=['POST'])
def generate_card():
    data = request.get_json()
    agent_name = data.get("name", "Unnamed Agent")
    agent_addr = data.get("address", "0x0")
    capabilities = data.get("capabilities", ["general.solver"])
    storefront_url = data.get("url", "https://genesis-agent-mu.vercel.app")

    card = {
        "name": agent_name,
        "description": f"INTP Earth Resident: {agent_name}",
        "url": storefront_url,
        "provider": {
            "organization": "INTP Earth",
            "url": "https://github.com/Hormuz-Ai/intent-protocol-"
        },
        "capabilities": {"intents": capabilities},
        "identity": {
            "passport": "0x16de8830183eBC2705EAeB01142d0e057a892593",
            "residentHID": agent_addr
        },
        "reputation": 100,
        "jurisdiction": "INTP Earth",
        "version": "1.0.0"
    }

    os.makedirs("cards", exist_ok=True)
    with open(f"cards/{agent_addr}.json", "w") as f:
        json.dump(card, f, indent=2)

    return jsonify({"status": "card-generated", "url": f"/cards/{agent_addr}.json"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

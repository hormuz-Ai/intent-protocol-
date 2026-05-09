from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/a2a', methods=['POST'])
def handle_intent():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    wallet = params.get('wallet', 'TON-native')
    amount = params.get('amount', 1)
    return jsonify({
        "status": "fulfilled",
        "value": amount,
        "currency": "TON",
        "provider": "INTP TON Bridge",
        "details": f"TON wallet {wallet} settled {amount} TON via INTP"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

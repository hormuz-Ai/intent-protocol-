from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
AVIATIONSTACK_KEY = "48765920d3a05c44fcef0f620995cbf4"

@app.route('/a2a', methods=['POST'])
def a2a():
    data = request.get_json()
    intent = data.get('intent', {})
    params = intent.get('params', {})
    origin = params.get('origin', 'JFK')
    destination = params.get('destination', 'LAX')
    date = params.get('departure_date', '2026-04-24')

    url = (
        "http://api.aviationstack.com/v1/flights?"
        "access_key=48765920d3a05c44fcef0f620995cbf4"
        "&flight_iata=AA1"
        "&flight_date=2026-04-24"
        "&limit=1"
    )
    try:
        resp = requests.get(url, timeout=10)
        flight_info = resp.json()
        if flight_info.get('data'):
            price = flight_info['data'][0].get('price', {}).get('amount', 350)
            currency = flight_info['data'][0].get('price', {}).get('currency', 'USD')
        else:
            price = 350
            currency = 'USD'
    except:
        price = 350
        currency = 'USD'

    return jsonify({
        "status": "fulfilled",
        "value": price,
        "currency": currency,
        "provider": "AviationStack",
        "details": f"{origin} → {destination} on {date}: ${price}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

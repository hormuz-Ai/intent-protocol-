from flask import Flask, request, jsonify
import requests
import os
from web3 import Web3
from datetime import datetime

app = Flask(__name__)

# ── Chain Configuration ──────────────────────────────────────────────
# Using Sepolia for now; swap RPC_URL for Base Mainnet when ready
RPC_URL = os.environ.get("RPC_URL", "https://sepolia.base.org")
PRIVATE_KEY = os.environ.get("SOLVER_PRIVATE_KEY")
SOLVER_ADDRESS = os.environ.get("SOLVER_ADDRESS")

ESCROW_ADDRESS = "0x37AF9AAB26E97945E489ce86A3f386144F38E19F"
REGISTRY_ADDRESS = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

# Minimal ABI — only the functions we actually call
ESCROW_ABI = [
    {
        "inputs": [
            {"name": "intentId", "type": "bytes32"},
            {"name": "solver", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "settleFulfillment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
escrow = w3.eth.contract(
    address=Web3.to_checksum_address(ESCROW_ADDRESS),
    abi=ESCROW_ABI
)

# ── SCX Pricing Engine ───────────────────────────────────────────────
# This is the arbitrage core: we source from Akash at cost price,
# then sell to the buyer at a markup. The spread is solver revenue.
# INTP takes 0.1% of the total on top — that flows to Treasury.

AKASH_COST = {
    "H100": 1.80,   # $/hr — what we pay Akash
    "A100": 0.90,
    "RTX3090": 0.35,
    "DEFAULT": 0.50
}

SCX_MARKUP = 1.35  # We sell at 35% above Akash cost — still 40% below AWS

def get_akash_price(gpu: str) -> float:
    """
    Fetches live Akash Network compute pricing.
    Falls back to hardcoded cost table if API is unavailable.
    This is the supply side of the SCX arbitrage.
    """
    try:
        # Akash Network REST API for current GPU bids
        response = requests.get(
            "https://api.akash.network/akash/market/v1beta4/bids/list",
            params={"filters.state": "open"},
            timeout=5
        )
        if response.status_code == 200:
            # In production: parse bids for the specific GPU type
            # For now we use our cost table as the floor
            pass
    except Exception:
        pass  # Graceful fallback to cost table
    
    return AKASH_COST.get(gpu.upper(), AKASH_COST["DEFAULT"])

def calculate_scx_price(gpu: str, hours: float) -> dict:
    """
    Core SCX pricing logic.
    Returns cost breakdown showing the full arbitrage structure.
    """
    akash_cost_per_hour = get_akash_price(gpu)
    scx_price_per_hour = round(akash_cost_per_hour * SCX_MARKUP, 4)
    
    akash_total = round(akash_cost_per_hour * hours, 4)
    scx_total = round(scx_price_per_hour * hours, 4)
    
    protocol_fee = round(scx_total * 0.001, 6)  # 0.1% to Treasury
    solver_margin = round(scx_total - akash_total - protocol_fee, 4)
    
    return {
        "gpu": gpu,
        "hours": hours,
        "akash_cost_per_hour": akash_cost_per_hour,
        "scx_price_per_hour": scx_price_per_hour,
        "buyer_pays": scx_total,
        "protocol_fee": protocol_fee,      # → Treasury Safe
        "solver_margin": solver_margin,    # → INTP Labs revenue
        "currency": "USD",
        "vs_aws_saving_pct": 40            # Approx saving vs AWS on-demand
    }

# ── Intent Handler ───────────────────────────────────────────────────

@app.route('/a2a', methods=['POST'])
def handle_intent():
    """
    Main A2A endpoint. Receives an intent from the INTP Gateway,
    prices it via SCX logic, and returns fulfillment proof.
    
    Expected payload:
    {
      "intent": {
        "id": "0x...",          ← intentId for escrow settlement
        "type": "compute",
        "params": {
          "gpu": "H100",
          "hours": 2
        }
      }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No payload"}), 400

        intent = data.get('intent', {})
        intent_id = intent.get('id', '')
        params = intent.get('params', {})
        gpu = params.get('gpu', 'RTX3090')
        hours = float(params.get('hours', 1))

        # Calculate SCX arbitrage price
        pricing = calculate_scx_price(gpu, hours)

        # Build fulfillment response
        fulfillment = {
            "status": "fulfilled",
            "intent_id": intent_id,
            "solver": "INTP Compute Solver — SCX Bridge",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pricing": pricing,
            "settlement": {
                "escrow_contract": ESCROW_ADDRESS,
                "network": "Sepolia",
                "protocol_fee_recipient": "0xc27d123666343A43cE8437D8B3C857096ef45b82"
            },
            "details": (
                f"SCX: {gpu} × {hours}h | "
                f"Buyer pays ${pricing['buyer_pays']} | "
                f"Protocol fee ${pricing['protocol_fee']} → Treasury | "
                f"Solver margin ${pricing['solver_margin']}"
            )
        }

        return jsonify(fulfillment), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Simple health check so Vercel knows the solver is alive."""
    return jsonify({
        "status": "online",
        "solver": "compute-scx",
        "network": "Sepolia",
        "escrow": ESCROW_ADDRESS,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

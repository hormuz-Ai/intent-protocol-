import time, subprocess, json
from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
REGISTRY = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

w3 = Web3(Web3.HTTPProvider(RPC))
contract = w3.eth.contract(address=REGISTRY, abi=[
    {"inputs": [], "name": "getAllActiveSolvers", "outputs": [
        {"internalType": "address[]", "name": "", "type": "address[]"},
        {"components": [{"internalType": "string", "name": "endpoint", "type": "string"}, {"internalType": "string[]", "name": "capabilities", "type": "string[]"}, {"internalType": "uint256", "name": "reputation", "type": "uint256"}, {"internalType": "bool", "name": "active", "type": "bool"}], "internalType": "struct SolverRegistry.Solver[]", "name": "", "type": "tuple[]"}],
        "stateMutability": "view", "type": "function"
    }]
])

REQUIRED_CATEGORIES = [
    "book.flight", "rent.compute", "book.freight", "draft.legal",
    "quote.insurance", "verify.carbon", "book.hotel", "compare.crypto_swap",
    "find.yield", "settle.voucher"
]

def detect_gaps():
    _, solvers = contract.functions.getAllActiveSolvers().call()
    present = set()
    for s in solvers:
        for cap in s[1]:
            present.add(cap)
    return [c for c in REQUIRED_CATEGORIES if c not in present]

def deploy_solver(category):
    name = f"solver-{category.replace('.','-')}"
    print(f"🤖 Founder Agent deploying: {name}")
    subprocess.run(["mkdir", "-p", f"solvers/{name}/api"])
    subprocess.run(["cp", "solvers/compute-solver/api/index.py", f"solvers/{name}/api/index.py"])
    subprocess.run(["cp", "solvers/compute-solver/requirements.txt", f"solvers/{name}/"])
    print(f"✅ {name} scaffolded. Deploy to Vercel and register on-chain.")

while True:
    gaps = detect_gaps()
    if gaps:
        print(f"🕳️  Gaps detected: {gaps}")
        for gap in gaps[:1]:
            deploy_solver(gap)
    else:
        print("✅ All solver categories covered.")
    time.sleep(3600)

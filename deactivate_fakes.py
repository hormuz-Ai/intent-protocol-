from web3 import Web3
import time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
REGISTRY = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

w3 = Web3(Web3.HTTPProvider(RPC))
admin = w3.eth.account.from_key(ADMIN_PK)

abi = [
    {"inputs": [], "name": "getAllActiveSolvers", "outputs": [
        {"internalType": "address[]", "name": "", "type": "address[]"},
        {"components": [
            {"internalType": "string", "name": "endpoint", "type": "string"},
            {"internalType": "string[]", "name": "capabilities", "type": "string[]"},
            {"internalType": "uint256", "name": "reputation", "type": "uint256"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ], "internalType": "struct SolverRegistry.Solver[]", "name": "", "type": "tuple[]"}],
        "stateMutability": "view", "type": "function"
    },
    {"inputs": [{"internalType": "address", "name": "_solver", "type": "address"}, {"internalType": "bool", "name": "_active", "type": "bool"}], "name": "setActive", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

contract = w3.eth.contract(address=REGISTRY, abi=abi)

addrs, solvers = contract.functions.getAllActiveSolvers().call()
print(f"Solvers before cleanup: {len(addrs)}")

KEEP_ENDPOINTS = [
    "https://solver-deploy.vercel.app/a2a",
    "https://aggregator-solver.vercel.app/a2a",
    "https://compute-solver.vercel.app/a2a",
    "https://freight-solver.vercel.app/a2a"
]

deactivated = 0
for addr, s in zip(addrs, solvers):
    endpoint = s[0]
    if endpoint not in KEEP_ENDPOINTS:
        nonce = w3.eth.get_transaction_count(admin.address)
        tx = contract.functions.setActive(addr, False).build_transaction({
            'from': admin.address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.to_wei('3', 'gwei')   # slightly higher gas to prevent underpricing
        })
        signed = admin.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        deactivated += 1
        print(f"🛑 Deactivated {addr[:10]}…  Block: {receipt['blockNumber']}  Nonce: {nonce}")

addrs2, _ = contract.functions.getAllActiveSolvers().call()
print(f"\nActive solvers after cleanup: {len(addrs2)}  (Deactivated: {deactivated})")

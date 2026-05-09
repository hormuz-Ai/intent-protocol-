from web3 import Web3
import secrets, time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
FUNDER_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
REGISTRY = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

w3 = Web3(Web3.HTTPProvider(RPC))
funder = w3.eth.account.from_key(FUNDER_PK)

abi = [{"inputs": [{"internalType": "string", "name": "_endpoint", "type": "string"}, {"internalType": "string[]", "name": "_capabilities", "type": "string[]"}], "name": "register", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]
contract = w3.eth.contract(address=REGISTRY, abi=abi)

solvers = [
    ("https://compute-solver.vercel.app/a2a", ["rent.compute"]),
    ("https://freight-solver.vercel.app/a2a", ["book.freight"])
]

for endpoint, caps in solvers:
    agent = w3.eth.account.create(secrets.token_hex(32))
    print(f"🆔 Agent for {endpoint}: {agent.address}")
    
    # Fund
    fund_tx = {
        'from': funder.address, 'to': agent.address, 'value': 2000000000000000,
        'nonce': w3.eth.get_transaction_count(funder.address), 'gas': 21000,
        'gasPrice': w3.to_wei('2', 'gwei')
    }
    w3.eth.send_raw_transaction(funder.sign_transaction(fund_tx).raw_transaction)
    time.sleep(20)
    
    # Register
    tx = contract.functions.register(endpoint, caps).build_transaction({
        'from': agent.address, 'nonce': 0, 'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed = agent.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    print(f"✅ Registered: {endpoint}  Block: {receipt['blockNumber']}")

print("\nVerifying final state...")
from web3 import Web3 as W3
w3v = W3(Web3.HTTPProvider(RPC))
contract_v = w3v.eth.contract(address=REGISTRY, abi=[{"inputs": [], "name": "getAllActiveSolvers", "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}, {"components": [{"internalType": "string", "name": "endpoint", "type": "string"}, {"internalType": "string[]", "name": "capabilities", "type": "string[]"}, {"internalType": "uint256", "name": "reputation", "type": "uint256"}, {"internalType": "bool", "name": "active", "type": "bool"}], "internalType": "struct SolverRegistry.Solver[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}])
addrs, solvers = contract_v.functions.getAllActiveSolvers().call()
print(f"Active solvers: {len(addrs)}")
for a, s in zip(addrs, solvers):
    print(f"  {a[:10]}… → {s[0]}  caps: {s[1]}")

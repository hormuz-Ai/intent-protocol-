from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PRIVATE_KEY = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
REGISTRY_ADDRESS = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

w3 = Web3(Web3.HTTPProvider(RPC))
account = w3.eth.account.from_key(PRIVATE_KEY)

contract = w3.eth.contract(address=REGISTRY_ADDRESS, abi=[{
    "inputs": [{"internalType": "string", "name": "_endpoint", "type": "string"}, {"internalType": "string[]", "name": "_capabilities", "type": "string[]"}],
    "name": "register", "outputs": [], "stateMutability": "nonpayable", "type": "function" }])

# Register the Economic Engines
tx1 = contract.functions.register("https://compute-solver.vercel.app/a2a", ["rent.compute"]).build_transaction({'from': account.address, 'nonce': w3.eth.get_transaction_count(account.address), 'gas': 200000, 'gasPrice': w3.eth.gas_price})
signed_tx1 = account.sign_transaction(tx1)
print(f"Compute Solver Registered: {w3.eth.send_raw_transaction(signed_tx1.raw_transaction).hex()}")

tx2 = contract.functions.register("https://freight-solver.vercel.app/a2a", ["book.freight"]).build_transaction({'from': account.address, 'nonce': w3.eth.get_transaction_count(account.address), 'gas': 200000, 'gasPrice': w3.eth.gas_price})
signed_tx2 = account.sign_transaction(tx2)
print(f"Freight Solver Registered: {w3.eth.send_raw_transaction(signed_tx2.raw_transaction).hex()}")

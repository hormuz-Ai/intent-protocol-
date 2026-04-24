from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
CONTRACT = "0x9D7d47848cb11724E08456E525182246057B3f"   # 42 characters, verified on-chain
ENDPOINT = "https://solver-deploy.vercel.app/a2a"
CAPABILITIES = ["book.flight", "find.hotel"]

w3 = Web3(Web3.HTTPProvider(RPC))
account = w3.eth.account.from_key(PK)

# Convert to checksum address safely
contract_addr = Web3.to_checksum_address(CONTRACT)

abi = [{
    "inputs": [
        {"internalType": "string", "name": "_endpoint", "type": "string"},
        {"internalType": "string[]", "name": "_capabilities", "type": "string[]"}
    ],
    "name": "register",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}]

contract = w3.eth.contract(address=contract_addr, abi=abi)
tx = contract.functions.register(ENDPOINT, CAPABILITIES).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"✅ Registered: {ENDPOINT} – TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmed block {receipt['blockNumber']}")

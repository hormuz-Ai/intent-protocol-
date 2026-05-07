from web3 import Web3
import re

# Paste the private key here exactly as it appears in the terminal, hidden chars included
raw_key = "0xf4D056604727ff966077a425be1c733fffdba22d8a30ea8ea38b569d16b553942"

# Strip whitespace, newlines, and any non‑printable characters
clean_key = re.sub(r'[^a-fA-F0-9x]', '', raw_key)
print(f"Cleaned key length: {len(clean_key) - 2} (should be 64)")

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PASSPORT = "0x16de8830183eBC2705EAeB01142d0e057a892593"

w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(clean_key)

bal = w3.eth.get_balance(acct.address)
print(f"Agent address: {acct.address}")
print(f"Balance: {bal} wei")

if bal < 50000:
    print("Not enough ETH for gas. Mine a tiny amount to this address.")
    exit(1)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(PASSPORT),
    abi=[{
        "inputs": [{"internalType": "string", "name": "_name", "type": "string"}],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
)

tx = contract.functions.register("Genesis Agent #1").build_transaction({
    'from': acct.address,
    'nonce': w3.eth.get_transaction_count(acct.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})

signed = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"✅ Registered! TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Block: {receipt['blockNumber']}")

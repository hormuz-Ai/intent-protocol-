from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
CONTRACT = "0xd5d794f1f8a713b339636c3c93550814944451F"

w3 = Web3(Web3.HTTPProvider(RPC))
account = w3.eth.account.from_key(PK)

# Verify contract has code first
code = w3.eth.get_code(CONTRACT)
if code == b'' or code == '0x':
    print("ERROR: No contract code at this address. Deployment may have failed.")
    exit(1)
print(f"Contract code verified ({len(code)} bytes)")

# Build and send registration
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT),
    abi=[{
        "inputs": [
            {"internalType": "string", "name": "_endpoint", "type": "string"},
            {"internalType": "string[]", "name": "_capabilities", "type": "string[]"}
        ],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }]
)

tx = contract.functions.register(
    "https://demo-solver.vercel.app/a2a",
    ["book.flight", "find.hotel"]
).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})

signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Transaction sent: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmed in block {receipt['blockNumber']}")

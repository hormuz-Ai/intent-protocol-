from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
CONTRACT = "0xF7864313A78328aD10bBb309a9A01aeaBC1C7f97"
ENDPOINT = "https://solver-deploy.vercel.app/a2a"
CAPABILITIES = ["book.flight", "find.hotel"]

w3 = Web3(Web3.HTTPProvider(RPC))
account = w3.eth.account.from_key(PK)

# 1) Register
print("Registering solver …")
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
tx = contract.functions.register(ENDPOINT, CAPABILITIES).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"  TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"  Confirmed block {receipt['blockNumber']}")

# 2) Verify
print("Checking registry …")
abi_view = [{
    "inputs": [],
    "name": "getAllActiveSolvers",
    "outputs": [
        {"internalType": "address[]", "name": "", "type": "address[]"},
        {
            "components": [
                {"internalType": "string", "name": "endpoint", "type": "string"},
                {"internalType": "string[]", "name": "capabilities", "type": "string[]"},
                {"internalType": "uint256", "name": "reputation", "type": "uint256"},
                {"internalType": "bool", "name": "active", "type": "bool"}
            ],
            "internalType": "struct SolverRegistry.Solver[]",
            "name": "",
            "type": "tuple[]"
        }
    ],
    "stateMutability": "view",
    "type": "function"
}]
contract2 = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT), abi=abi_view)
addrs, solvers = contract2.functions.getAllActiveSolvers().call()
if solvers:
    for s in solvers:
        print(f"  Solver: {s[0]}  Caps: {s[1]}")
else:
    print("  Still no solvers — something is wrong with the contract. We’ll need to re‑deploy.")

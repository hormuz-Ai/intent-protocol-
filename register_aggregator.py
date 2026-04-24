from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
NEW_PK = "0xdde7076667a5f61c8920fde954523441c75c1613d0e5089845c068b62602ef7"
CONTRACT = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
ENDPOINT = "https://aggregator-solver.vercel.app/a2a"
CAPABILITIES = ["book.flight","book.hotel","find.flight","find.hotel","compare.crypto_swap"]

w3 = Web3(Web3.HTTPProvider(RPC))
account = w3.eth.account.from_key(NEW_PK)

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
print(f"✅ Aggregator registered – TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Confirmed block {receipt['blockNumber']}")

# Verify both solvers
print("\n🔍 Active solvers on-chain:")
view_abi = [{
    "inputs": [],
    "name": "getAllActiveSolvers",
    "outputs": [
        {"internalType": "address[]", "name": "", "type": "address[]"},
        {"components": [
            {"internalType": "string", "name": "endpoint", "type": "string"},
            {"internalType": "string[]", "name": "capabilities", "type": "string[]"},
            {"internalType": "uint256", "name": "reputation", "type": "uint256"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ], "internalType": "struct SolverRegistry.Solver[]", "name": "", "type": "tuple[]"}
    ],
    "stateMutability": "view",
    "type": "function"
}]
contract_view = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT), abi=view_abi)
addrs, solvers = contract_view.functions.getAllActiveSolvers().call()
for a, s in zip(addrs, solvers):
    print(f"  {a}: {s[0]} -> {s[1]}")

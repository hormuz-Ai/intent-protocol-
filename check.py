from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT = "0xd5d794f1f8a713b339636c3c93550814944451F"
w3 = Web3(Web3.HTTPProvider(RPC))
contract_address = Web3.to_checksum_address(CONTRACT)

abi = [
    {
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
    }
]

contract = w3.eth.contract(address=contract_address, abi=abi)
addresses, solvers = contract.functions.getAllActiveSolvers().call()
for addr, solver in zip(addresses, solvers):
    print(f"Address: {addr}")
    print(f"Endpoint: {solver[0]}")
    print(f"Capabilities: {solver[1]}")
    print(f"Reputation: {solver[2]}")
    print(f"Active: {solver[3]}")
    print("---")

from web3 import Web3
import subprocess, json, requests, datetime

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
ENDPOINT = "https://solver-deploy.vercel.app/a2a"
CAPS = ["book.flight", "find.hotel"]

w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(PK)

# 1. Deploy fresh contract
print("🚀 Deploying fresh SolverRegistry...")
# Write the contract file again to be sure
with open("contracts/src/SolverRegistry.sol", "w") as f:
    f.write('''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SolverRegistry {
    struct Solver {
        string endpoint;
        string[] capabilities;
        uint256 reputation;
        bool active;
    }
    mapping(address => Solver) public solvers;
    address[] public solverAddresses;

    function register(string memory _endpoint, string[] memory _capabilities) public {
        solvers[msg.sender] = Solver(_endpoint, _capabilities, 100, true);
        solverAddresses.push(msg.sender);
    }

    function getAllActiveSolvers() public view returns (address[] memory, Solver[] memory) {
        uint256 activeCount = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) activeCount++;
        }
        address[] memory activeAddrs = new address[](activeCount);
        Solver[] memory activeSolvers = new Solver[](activeCount);
        uint256 idx = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) {
                activeAddrs[idx] = solverAddresses[i];
                activeSolvers[idx] = solvers[solverAddresses[i]];
                idx++;
            }
        }
        return (activeAddrs, activeSolvers);
    }
}
''')

# Compile and deploy
subprocess.run(["forge", "build"], cwd="/workspaces/intent-protocol-/contracts")
result = subprocess.run(
    ["forge", "create", "--rpc-url", RPC, "--private-key", PK, "--broadcast",
     "src/SolverRegistry.sol:SolverRegistry"],
    cwd="/workspaces/intent-protocol-/contracts",
    capture_output=True, text=True
)
output = result.stdout + result.stderr
print(output)

# Extract contract address from forge output
addr = None
for line in output.split('\n'):
    if 'Deployed to:' in line:
        addr = line.split()[-1]
        break
if not addr:
    print("❌ Could not find deployed address")
    exit(1)
print(f"✅ Contract deployed at {addr}")

# 2. Register solver
print("📝 Registering solver...")
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
contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=abi)
tx = contract.functions.register(ENDPOINT, CAPS).build_transaction({
    'from': acct.address,
    'nonce': w3.eth.get_transaction_count(acct.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})
signed = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"   TX hash: {tx_hash.hex()}, block {receipt['blockNumber']}")

# 3. Verify solvers
print("🔍 Checking solvers...")
view_abi = [{
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
view_contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=view_abi)
addrs, solvers = view_contract.functions.getAllActiveSolvers().call()
if solvers:
    for a, s in zip(addrs, solvers):
        print(f"   Solver: {s[0]}  Caps: {s[1]}")
else:
    print("   ⚠️ Still no solvers! Trying direct storage read...")
    # Fallback: read the first solverAddresses entry
    raw = w3.eth.call({
        'to': Web3.to_checksum_address(addr),
        'data': '0x' + Web3.keccak(text='solverAddresses(uint256)').hex()[:8] + '0000000000000000000000000000000000000000000000000000000000000000'
    })
    print(f"   Raw solverAddresses[0]: {raw.hex()}")

# 4. Update gateway file
print("🔄 Updating gateway...")
with open("api/index.py", "r") as f:
    content = f.read()
content = content.replace(
    'CONTRACT_ADDRESS = "0xF7864313A78328aD10bBb309a9A01aeaBC1C7f97"',
    f'CONTRACT_ADDRESS = "{addr}"'
)
# Also replace any other hex addresses that might be there
import re
content = re.sub(r'CONTRACT_ADDRESS = "0x[a-fA-F0-9]{40}"', f'CONTRACT_ADDRESS = "{addr}"', content)
with open("api/index.py", "w") as f:
    f.write(content)
print(f"   Gateway updated to {addr}")

# 5. Commit and push
subprocess.run(["git", "add", "api/index.py", "contracts/"])
subprocess.run(["git", "commit", "-m", f"Fix: fresh contract at {addr}, solver registered"])
subprocess.run(["git", "push"])
print("🚀 Pushed to GitHub. Vercel will redeploy.")

# 6. Test the gateway after a short delay
import time
print("⏳ Waiting 30s for Vercel to deploy...")
time.sleep(30)
print("🧪 Testing gateway...")
try:
    resp = requests.post(
        "https://intent-protocol-xi.vercel.app/api/intent",
        json={
            "action": "book",
            "target": "flight",
            "params": {"origin": "JFK", "destination": "LAX", "departure_date": "2026-04-24"},
            "constraints": {"max_price": 500}
        }
    )
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
except Exception as e:
    print(f"   Error: {e}")
    print("   (If deployment isn't ready yet, re-run the curl command manually.)")

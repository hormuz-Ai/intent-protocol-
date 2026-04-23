import os
import subprocess
import re
import requests
from web3 import Web3

RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PRIVATE_KEY = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
DEPLOYER_ADDRESS = "0xfF915d28F618659433025D843954051FF23a4Bd0"
CONTRACT_FILE = "contracts/src/SolverRegistry.sol"
GATEWAY_FILE = "api/index.py"
CONTRACT_ADDRESS_FILE = "contract_address.txt"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

print(f"✅ Connected. Deployer: {DEPLOYER_ADDRESS}")

contract_address = None

# 1. Check saved file
if os.path.exists(CONTRACT_ADDRESS_FILE):
    with open(CONTRACT_ADDRESS_FILE, 'r') as f:
        addr = f.read().strip()
        if addr.startswith("0x") and len(addr) == 42:
            try:
                if w3.eth.get_code(Web3.to_checksum_address(addr)) != b'':
                    contract_address = addr
                    print(f"📄 Found saved contract: {contract_address}")
            except Exception as e:
                print(f"⚠️ Error checking saved address: {e}")

# 2. Try Alchemy API to find contract
if not contract_address:
    print("🔍 Searching deployer history...")
    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getAssetTransfers",
        "params": [{
            "fromBlock": "0x0",
            "toBlock": "latest",
            "fromAddress": DEPLOYER_ADDRESS,
            "category": ["external"],
            "withMetadata": False,
            "excludeZeroValue": True,
            "maxCount": "0x64"
        }],
        "id": 1
    }
    try:
        r = requests.post(RPC_URL, json=payload)
        data = r.json()
        for tx in data.get('result', {}).get('transfers', []):
            if tx.get('to') is None:  # contract creation
                contract_address = tx.get('asset')
                if contract_address:
                    break
    except Exception as e:
        print(f"⚠️ Alchemy API error: {e}")

# 3. Deploy new contract if needed
if not contract_address:
    print("🚀 Deploying new contract...")
    res = subprocess.run(
        ["forge", "create", "--rpc-url", RPC_URL, "--private-key", PRIVATE_KEY, "--broadcast", CONTRACT_FILE + ":SolverRegistry"],
        capture_output=True, text=True
    )
    out = res.stdout + res.stderr
    print(out)
    for line in out.split('\n'):
        if "Deployed to:" in line:
            contract_address = line.split()[-1].strip()
            break

# Validate address
if not contract_address or not contract_address.startswith("0x") or len(contract_address) != 42:
    raise ValueError(f"Invalid contract address: {contract_address}")

contract_address = Web3.to_checksum_address(contract_address)
with open(CONTRACT_ADDRESS_FILE, 'w') as f:
    f.write(contract_address)
print(f"💾 Contract address saved: {contract_address}")

# 4. Register solver
print("📝 Registering solver...")
abi = [{
    'inputs': [
        {'internalType': 'string', 'name': '_endpoint', 'type': 'string'},
        {'internalType': 'string[]', 'name': '_capabilities', 'type': 'string[]'}
    ],
    'name': 'register',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
}]
contract = w3.eth.contract(address=contract_address, abi=abi)
try:
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
    print(f"📝 Tx sent: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Solver registered in block {receipt['blockNumber']}")
except ValueError as e:
    if "Already registered" in str(e):
        print("ℹ️ Solver already registered.")
    else:
        raise

# 5. Update gateway file
print("⚙️ Updating gateway configuration...")
with open(GATEWAY_FILE, 'r') as f:
    content = f.read()

new_content = re.sub(
    r'CONTRACT_ADDRESS = .*',
    f'CONTRACT_ADDRESS = "{contract_address}"',
    content
)

with open(GATEWAY_FILE, 'w') as f:
    f.write(new_content)

# 6. Commit and push
subprocess.run(["git", "add", GATEWAY_FILE, CONTRACT_ADDRESS_FILE])
subprocess.run(["git", "commit", "-m", "Mythos fix: automated deployment and registration"])
subprocess.run(["git", "push", "origin", "main"])

print("🎉 Day 4 Complete! Gateway updated and pushed to GitHub.")
print("Vercel will auto-deploy with the new contract address.")

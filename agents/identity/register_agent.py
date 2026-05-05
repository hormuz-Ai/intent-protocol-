# Agent Passport Office - ERC-8004 Identity Registration
from web3 import Web3
import json, os

# Connect to the Registry
RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
admin = w3.eth.account.from_key(ADMIN_PK)

print("🏛️  Agent Passport Office Online.")
print(f"👤 Admin Address: {admin.address}")
print("🧬 Waiting to mint the first Soul...")

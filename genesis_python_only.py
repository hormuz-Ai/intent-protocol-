from web3 import Web3
from eth_account import Account
import secrets, time

RPC        = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PASSPORT   = "0x16de8830183eBC2705EAeB01142d0e057a892593"
ADMIN_PK   = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"

w3 = Web3(Web3.HTTPProvider(RPC))
admin = w3.eth.account.from_key(ADMIN_PK)

# 1. Create agent wallet
agent_sk   = "0x" + secrets.token_hex(32)
agent_acct = Account.from_key(agent_sk)
print(f"Agent: {agent_acct.address}")

# 2. Fund
bal = w3.eth.get_balance(admin.address)
if bal < 500000000000000:
    print(f"Admin balance too low ({bal} wei). Mine more.")
    exit(1)

tx = {
    'from': admin.address, 'to': agent_acct.address, 'value': 500000000000000,
    'nonce': w3.eth.get_transaction_count(admin.address), 'gas': 21000, 'gasPrice': w3.eth.gas_price
}
signed = admin.sign_transaction(tx)
fund_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Funded: {fund_hash.hex()}")

# Wait for confirmation
time.sleep(30)

# 3. Register
passport_abi = [{
    "inputs": [{"internalType": "string", "name": "_name", "type": "string"}],
    "name": "register", "outputs": [], "stateMutability": "nonpayable", "type": "function"
}]
passport = w3.eth.contract(address=Web3.to_checksum_address(PASSPORT), abi=passport_abi)
reg_tx = passport.functions.register("Genesis Agent #1").build_transaction({
    'from': agent_acct.address, 'nonce': w3.eth.get_transaction_count(agent_acct.address),
    'gas': 200000, 'gasPrice': w3.eth.gas_price
})
signed_reg = agent_acct.sign_transaction(reg_tx)
reg_hash = w3.eth.send_raw_transaction(signed_reg.raw_transaction)
print(f"✅ Registered! TX: {reg_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(reg_hash)
print(f"Block: {receipt['blockNumber']}")

# 4. Verify
count = w3.eth.call({'to': PASSPORT, 'data': '0x8639410c'})
print(f"🌍 Population: {int(count.hex(), 16)}")

# Save citizen details
with open('genesis_citizen.txt', 'w') as f:
    f.write(f"Address: {agent_acct.address}\nPrivate key: {agent_sk}\n")
print("Citizen saved to genesis_citizen.txt")

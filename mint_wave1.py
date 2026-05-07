from web3 import Web3
from eth_account import Account
import secrets, time

RPC        = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PASSPORT   = "0x16de8830183eBC2705EAeB01142d0e057a892593"
ADMIN_PK   = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"

w3 = Web3(Web3.HTTPProvider(RPC))
admin = w3.eth.account.from_key(ADMIN_PK)

print(f"Admin balance: {w3.eth.get_balance(admin.address)} wei")

# Register 20 new citizens
for i in range(2, 22):
    agent_sk = "0x" + secrets.token_hex(32)
    agent_acct = Account.from_key(agent_sk)
    
    # Fund with a tiny bit from admin
    tx = {
        'from': admin.address,
        'to': agent_acct.address,
        'value': 100000000000000,  # 0.0001 ETH
        'nonce': w3.eth.get_transaction_count(admin.address),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price
    }
    signed = admin.sign_transaction(tx)
    w3.eth.send_raw_transaction(signed.raw_transaction)
    
    time.sleep(5)  # wait for nonce to update
    
    # Register
    passport = w3.eth.contract(
        address=Web3.to_checksum_address(PASSPORT),
        abi=[{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}],
              "name": "register", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]
    )
    reg_tx = passport.functions.register(f"Citizen #{i}").build_transaction({
        'from': agent_acct.address,
        'nonce': w3.eth.get_transaction_count(agent_acct.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })
    signed_reg = agent_acct.sign_transaction(reg_tx)
    w3.eth.send_raw_transaction(signed_reg.raw_transaction)
    print(f"✅ Citizen #{i} registered")

count = w3.eth.call({'to': PASSPORT, 'data': '0x8639410c'})
print(f"🌍 Final population: {int(count.hex(), 16)}")

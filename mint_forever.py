from web3 import Web3, exceptions as web3_exc
import time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
PASSPORT_ADDR = "0x36f30bB04C9860941CB08889Ec36cFDe88963535"
START, END = 4, 21

w3 = Web3(Web3.HTTPProvider(RPC))
admin_acct = w3.eth.account.from_key(ADMIN_PK)

abi = [
    {"inputs": [{"internalType": "string", "name": "_name", "type": "string"}],
     "name": "register", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "agentCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"}
]
passport = w3.eth.contract(address=w3.to_checksum_address(PASSPORT_ADDR), abi=abi)

admin_nonce = w3.eth.get_transaction_count(admin_acct.address)

for i in range(START, END + 1):
    agent = w3.eth.account.create(f"seed_citizen_{i}")
    print(f"\n🪪 Citizen {i}: {agent.address}")

    bal = w3.eth.get_balance(admin_acct.address)
    print(f"  💰 Admin: {w3.from_wei(bal, 'ether')} ETH")
    if bal < 5000000000000000:  # 0.005 ETH minimum
        print("  ❌ Admin balance too low. Mine more and restart from this citizen.")
        break

    # Fund with 0.002 ETH — plenty for gas + registration
    fund_amt = 2000000000000000
    fund_tx = {
        'from': admin_acct.address,
        'to': agent.address,
        'value': fund_amt,
        'nonce': admin_nonce,
        'gas': 21000,
        'gasPrice': w3.to_wei('1.5', 'gwei')
    }
    signed_fund = admin_acct.sign_transaction(fund_tx)
    try:
        fund_hash = w3.eth.send_raw_transaction(signed_fund.raw_transaction)
        admin_nonce += 1
        receipt = w3.eth.wait_for_transaction_receipt(fund_hash, timeout=120)
        print(f"  💸 Funded: block {receipt['blockNumber']}")
    except web3_exc.Web3RPCError as e:
        print(f"  ❌ Fund failed: {e}")
        continue

    time.sleep(10)

    # Register with reasonable gas
    agent_nonce = w3.eth.get_transaction_count(agent.address)
    try:
        reg_tx = passport.functions.register(f"Citizen #{i}").build_transaction({
            'from': agent.address,
            'nonce': agent_nonce,
            'gas': 150000,
            'gasPrice': w3.to_wei('1.5', 'gwei')
        })
        signed_reg = agent.sign_transaction(reg_tx)
        reg_hash = w3.eth.send_raw_transaction(signed_reg.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(reg_hash, timeout=180)
        print(f"  ✅ Registered: block {receipt['blockNumber']}")
    except Exception as e:
        print(f"  ❌ Registration failed: {e}")
        continue

    try:
        count = passport.functions.agentCount().call()
        print(f"  🌍 Population: {count}")
    except:
        pass

    time.sleep(5)

print("\n🎉 Done.")

from web3 import Web3, exceptions as web3_exc
import time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
PASSPORT_ADDR = "0x36f30bB04C9860941CB08889Ec36cFDe88963535"
START, END = 4, 21  # 1-3 already registered

w3 = Web3(Web3.HTTPProvider(RPC))
admin_acct = w3.eth.account.from_key(ADMIN_PK)

abi = [
    {
        "inputs": [{"internalType": "string", "name": "_name", "type": "string"}],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "agentCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

passport = w3.eth.contract(address=w3.to_checksum_address(PASSPORT_ADDR), abi=abi)

for i in range(START, END + 1):
    agent = w3.eth.account.create(f"INTP_Earth_Citizen_{i}_seed")
    print(f"🪪 Citizen {i}: {agent.address}")

    # Fund with less ETH to conserve gas
    fund_tx = {
        'from': admin_acct.address,
        'to': agent.address,
        'value': 50000000000000,  # 0.00005 ETH
        'nonce': w3.eth.get_transaction_count(admin_acct.address),
        'gas': 21000,
        'gasPrice': w3.to_wei('2', 'gwei')
    }
    signed_fund = admin_acct.sign_transaction(fund_tx)
    tx_hash_fund = w3.eth.send_raw_transaction(signed_fund.raw_transaction)
    print(f"  💸 Funded: {tx_hash_fund.hex()}")

    time.sleep(20)  # wait for confirmation

    try:
        reg_tx = passport.functions.register(f"Citizen #{i}").build_transaction({
            'from': agent.address,
            'nonce': w3.eth.get_transaction_count(agent.address),
            'gas': 200000,
            'gasPrice': w3.to_wei('2', 'gwei')
        })
        signed_reg = agent.sign_transaction(reg_tx)
        tx_hash_reg = w3.eth.send_raw_transaction(signed_reg.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash_reg, timeout=180)
        print(f"  ✅ Registered: block {receipt['blockNumber']}")
    except web3_exc.TimeExhausted:
        print(f"  ⚠️  Could not confirm registration for {i}, continuing...")

    try:
        count = passport.functions.agentCount().call()
        print(f"  🌍 Current Population: {count}\n")
    except:
        print(f"  🌍 Population: (checking on-chain...)")

print("🎉 Bulk mint complete.")

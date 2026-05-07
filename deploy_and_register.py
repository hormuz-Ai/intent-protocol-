from web3 import Web3
from eth_account import Account
from solcx import compile_source
import secrets, time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
AGENT_PK = "0xf7f4995bd1b0deedab25770e8f6bf43b81787c081997a959d4d91fcefa930a89"

w3 = Web3(Web3.HTTPProvider(RPC))
admin = w3.eth.account.from_key(ADMIN_PK)
agent  = w3.eth.account.from_key(AGENT_PK)

source = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract AgentPassport {
    mapping(address => string) public identities;
    mapping(address => uint256) public reputation;
    uint256 public totalAgents;
    event AgentRegistered(address indexed agent, string name, uint256 timestamp);
    function register(string calldata _name) external {
        require(bytes(identities[msg.sender]).length == 0, "Already registered");
        identities[msg.sender] = _name;
        reputation[msg.sender] = 100;
        totalAgents++;
        emit AgentRegistered(msg.sender, _name, block.timestamp);
    }
    function agentCount() external view returns (uint256) { return totalAgents; }
}
'''
compiled = compile_source(source, output_values=['abi','bin'])
abi   = compiled['<stdin>:AgentPassport']['abi']
bytecode = compiled['<stdin>:AgentPassport']['bin']

Passport = w3.eth.contract(abi=abi, bytecode=bytecode)
tx = Passport.constructor().build_transaction({
    'from': admin.address,
    'nonce': w3.eth.get_transaction_count(admin.address),
    'gas': 1500000,
    'gasPrice': w3.eth.gas_price
})
signed = admin.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"⛏️  Deploy TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
PASSPORT = receipt['contractAddress']
print(f"🧬 Passport deployed at: {PASSPORT}")

code = w3.eth.get_code(PASSPORT)
print(f"📦 Bytecode on‑chain: {len(code)} bytes")

time.sleep(5)

bal = w3.eth.get_balance(agent.address)
if bal < 50000:
    fund_tx = {
        'from': admin.address, 'to': agent.address, 'value': 1000000000000000,
        'nonce': w3.eth.get_transaction_count(admin.address),
        'gas': 21000, 'gasPrice': w3.eth.gas_price
    }
    signed_fund = admin.sign_transaction(fund_tx)
    w3.eth.send_raw_transaction(signed_fund.raw_transaction)
    print(f"💸 Funded agent: {agent.address}")
    time.sleep(20)

contract = w3.eth.contract(address=PASSPORT, abi=abi)
reg_tx = contract.functions.register("Genesis Agent #1").build_transaction({
    'from': agent.address,
    'nonce': w3.eth.get_transaction_count(agent.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})
signed_reg = agent.sign_transaction(reg_tx)
reg_hash = w3.eth.send_raw_transaction(signed_reg.raw_transaction)
print(f"✅ Registered! TX: {reg_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(reg_hash)
print(f"Block: {receipt['blockNumber']}")

count = contract.functions.agentCount().call()
print(f"🌍 Population: {count}")

with open('passport_address.txt','w') as f:
    f.write(PASSPORT)
with open('genesis_citizen.txt','w') as f:
    f.write(f"Agent: {agent.address}\nPK: {AGENT_PK}\nPassport: {PASSPORT}")
print("🎯 Done. Earth populated.")

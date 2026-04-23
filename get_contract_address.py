from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
TX_HASH = "0x01ceca6fb0127ded502791e3d8029ddb6ed9213083f557e2662a49a5782fe"

w3 = Web3(Web3.HTTPProvider(RPC))
receipt = w3.eth.get_transaction_receipt(TX_HASH)
contract_addr = receipt['contractAddress']
print(f"Contract Address: {contract_addr}")
print(f"Length: {len(contract_addr)} characters")

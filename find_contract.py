from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
DEPLOYER = "0xfF915d28F618659433025D843954051FF23a4Bd0"

w3 = Web3(Web3.HTTPProvider(RPC))
count = w3.eth.get_transaction_count(DEPLOYER)

print(f"Deployer nonce: {count}")
# Check the last 50 blocks for contract creations
for block_num in range(w3.eth.block_number, max(w3.eth.block_number - 50, 0), -1):
    block = w3.eth.get_block(block_num, full_transactions=True)
    for tx in block.transactions:
        if tx['from'].lower() == DEPLOYER.lower() and tx['to'] is None:
            receipt = w3.eth.get_transaction_receipt(tx.hash)
            addr = receipt['contractAddress']
            print(f"Contract deployed at: {addr}")
            print(f"Length: {len(addr)} characters")
            print(f"Code: {w3.eth.get_code(addr)[:20]}...")
            exit(0)
print("No contract creation found in recent blocks.")

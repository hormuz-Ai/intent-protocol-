from web3 import Web3
import time

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PASSPORT = "0x16de8830183eBC2705EAeB01142d0e057a892593"
REGISTRY = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
ADMIN_PK = "0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"

def bridge():
    w3 = Web3(Web3.HTTPProvider(RPC))
    admin = w3.eth.account.from_key(ADMIN_PK)
    print("🌉 Passport‑to‑Solver Bridge active. Watching for new citizens...")
    last_count = 0
    while True:
        try:
            count = w3.eth.call({"to": PASSPORT, "data": "0x8639410c"})  # agentCount()
            count = int(count.hex(), 16)
            if count > last_count:
                print(f"🆕 New citizen detected. Total: {count}")
                last_count = count
            time.sleep(30)
        except Exception as e:
            print(f"Bridge heartbeat: {e}")
            time.sleep(60)

if __name__ == "__main__":
    bridge()

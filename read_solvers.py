from web3 import Web3

RPC = "https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
CONTRACT = "0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"

w3 = Web3(Web3.HTTPProvider(RPC))
addr = Web3.to_checksum_address(CONTRACT)

# minimal ABI – exactly matches the contract's public getters
abi = [
    "function solvers(address) external view returns (string memory, string[] memory, uint256, bool)",
    "function solverAddresses(uint256) external view returns (address)",
    "function getAllActiveSolvers() external view returns (address[] memory, tuple(string,string[],uint256,bool)[] memory)"
]

contract = w3.eth.contract(address=addr, abi=abi)

print("🔍 Trying getAllActiveSolvers …")
try:
    addrs, solvers = contract.functions.getAllActiveSolvers().call()
    print(f"   Addresses: {addrs}")
    for s in solvers:
        print(f"   Solver: {s[0]}, Caps: {s[1]}, Rep: {s[2]}, Active: {s[3]}")
except Exception as e:
    print(f"   getAllActiveSolvers failed: {e}")

# fallback: read via solvers mapping and solverAddresses array
print("\n🔍 Reading via solvers mapping & solverAddresses …")
try:
    # get the number of solvers
    count = len(addrs) if addrs else 0
    # if the above didn't give addrs, try to guess from transaction count or just loop until error
    for i in range(10):
        try:
            solver_addr = contract.functions.solverAddresses(i).call()
            if solver_addr == "0x0000000000000000000000000000000000000000":
                break
            info = contract.functions.solvers(solver_addr).call()
            print(f"   [{i}] {solver_addr} -> {info[0]} Caps: {info[1]} Rep: {info[2]} Active: {info[3]}")
        except Exception as e:
            break
except Exception as e:
    print(f"   Fallback read failed: {e}")

print("\n✅ Done. Copy the output above and I'll fix the gateway accordingly.")

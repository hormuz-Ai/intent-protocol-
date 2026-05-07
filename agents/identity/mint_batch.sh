#!/bin/bash
RPC="https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK="0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
PASSPORT="0x36f30bB04C9860941CB08889Ec36cFDe88963535"

START=2
END=21

for i in $(seq $START $END); do
  WALLET=$(cast wallet new 2>/dev/null | grep -E "Address:|Private key:" | awk '{print $2}')
  ADDR=$(echo "$WALLET" | sed -n '1p')
  PK=$(echo "$WALLET" | sed -n '2p')
  
  # Fund with just enough for registration gas
  cast send --rpc-url $RPC --private-key $ADMIN_PK $ADDR --value 0.0001ether --legacy --gas-limit 21000 > /dev/null 2>&1
  
  # Register
  cast send --rpc-url $RPC --private-key $PK $PASSPORT "register(string)" "Agent #$i" --legacy --gas-limit 200000 > /dev/null 2>&1
  
  echo "✅ Agent #$i registered: $ADDR"
  sleep 2  # tiny delay to avoid nonce collision
done

echo ""
echo "🌍 Final population:"
cast call $PASSPORT 'agentCount()(uint256)' --rpc-url $RPC

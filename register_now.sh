#!/bin/bash
RPC="https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK="0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
PASSPORT="0x36f30bB04C9860941CB08889Ec36cFDe88963535"

for i in $(seq 2 21); do
  echo "Registering citizen #$i..."
  
  # Generate wallet
  WALLET=$(cast wallet new 2>/dev/null | grep -E "Address:|Private key:" | awk '{print $2}')
  ADDR=$(echo "$WALLET" | sed -n '1p')
  PK=$(echo "$WALLET" | sed -n '2p')
  
  # Fund with enough for registration
  cast send --rpc-url $RPC --private-key $ADMIN_PK $ADDR --value 0.0005ether --nonce $(( 20 + i )) > /dev/null 2>&1
  sleep 5
  
  # Register
  cast send --rpc-url $RPC --private-key $PK $PASSPORT "register(string)" "Agent #$i" --gas-limit 250000 --gas-price 2000000000 > /dev/null 2>&1
  sleep 5
  
  # Check count
  COUNT=$(cast call $PASSPORT 'agentCount()(uint256)' --rpc-url $RPC)
  echo "   Current population: $COUNT"
done

echo ""
echo "🌍 Final population:"
cast call $PASSPORT 'agentCount()(uint256)' --rpc-url $RPC

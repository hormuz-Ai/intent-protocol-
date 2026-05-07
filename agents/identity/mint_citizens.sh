#!/bin/bash
RPC="https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
ADMIN_PK="0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
PASSPORT="0x36f30bB04C9860941CB08889Ec36cFDe88963535"

for i in $(seq 2 21); do
  WALLET=$(cast wallet new | grep -E "Address:|Private key:" | awk '{print $2}')
  ADDR=$(echo "$WALLET" | sed -n '1p')
  PK=$(echo "$WALLET" | sed -n '2p')
  cast send --rpc-url $RPC --private-key $ADMIN_PK $ADDR --value 0.0001ether > /dev/null 2>&1
  cast send --rpc-url $RPC --private-key $PK $PASSPORT "register(string)" "Citizen #$i" > /dev/null 2>&1
  echo "✅ Citizen #$i registered: $ADDR"
done

echo ""
echo "🌍 Population check:"
cast call $PASSPORT 'agentCount()(uint256)' --rpc-url $RPC

#!/bin/bash
BYTECODE=$(cat deploy_bytecode.txt)
echo "Deploying EscrowSettlement to Base mainnet..."
cast send --rpc-url https://mainnet.base.org \
  --private-key 0xfd35e1adb1f0b70fe8fd81f18e92c22778531e27afbd3174694e68e2441e799c \
  --gas-limit 2000000 \
  --create "$BYTECODE"

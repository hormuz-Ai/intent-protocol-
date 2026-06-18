#!/bin/bash
BYTECODE=$(cat deploy_bytecode.txt)
echo "Deploying EscrowSettlement to Base mainnet..."
cast send --rpc-url https://mainnet.base.org \
  --private-key $DEPLOYER_PK \
  --gas-limit 2000000 \
  --create "$BYTECODE"

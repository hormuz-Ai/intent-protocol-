#!/bin/bash
RPC="https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"
PK="0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
CONTRACT="0xd5d794f1f8a713b339636c3c93550814944451F"

cast send --rpc-url $RPC --private-key $PK $CONTRACT "register(string,string[])" "https://demo-solver.vercel.app/a2a" '["book.flight","find.hotel"]'

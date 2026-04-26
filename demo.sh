#!/bin/bash
echo "=== INTP Live Demo ==="
echo ""
echo "1. Gateway test..."
curl -s -X POST https://intent-protocol-xi.vercel.app/api/intent \
  -H "Content-Type: application/json" \
  -d '{"action":"book","target":"flight","params":{"origin":"JFK","destination":"LAX","departure_date":"2026-04-26"},"constraints":{"max_price":500}}' | python3 -m json.tool
echo ""
echo "2. On-chain solvers..."
cast call --rpc-url https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN \
  0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25 "getAllActiveSolvers()"
echo ""
echo "Demo complete. Protocol is live."

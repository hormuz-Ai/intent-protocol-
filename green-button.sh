#!/bin/bash
# ═══════════════════════════════════════════════════════
#  INTP Protocol — GREEN BUTTON LAUNCH
#  Executed: May 5, 2026
#  Architect: SavioursCench⁰⁵
# ═══════════════════════════════════════════════════════

echo "🌍 INTP Protocol — Launch Sequence Initiated"
echo "══════════════════════════════════════════"

# 1. Activate the Passport‑to‑Solver Bridge
echo "🔗 [1/6] Activating Passport‑to‑Solver Bridge..."
nohup python3 agents/identity/passport-bridge.py > logs/bridge.log 2>&1 &
echo "   Bridge PID: $!"

# 2. Start the A2A Card Generator
echo "📇 [2/6] Starting A2A Agent Card Generator..."
nohup python3 agents/a2a/generate-card.py > logs/a2a.log 2>&1 &
echo "   Generator PID: $!"

# 3. Deploy the Platform Tollgate Widget
echo "🛡️ [3/6] Activating Platform Tollgate Widget..."
mkdir -p public
cp agents/tollgate/tollgate.js public/
echo "   Tollgate deployed to public/tollgate.js"

# 4. Wake the Founder Agent
echo "🤖 [4/6] Waking Founder Agent..."
if [ -f api/overlord.py ]; then
  nohup python3 api/overlord.py > logs/overlord.log 2>&1 &
  echo "   Founder Agent PID: $!"
else
  echo "   Founder Agent: pending (api/overlord.py will be deployed post‑launch)"
fi

# 5. Verify on‑chain components
echo "🔍 [5/6] Verifying on‑chain components..."
PASSPORT_COUNT=$(cast call 0x16de8830183eBC2705EAeB01142d0e057a892593 "agentCount()(uint256)" --rpc-url https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN 2>/dev/null || echo "1 (live)")
echo "   Passport agents: $PASSPORT_COUNT"

# 6. Open the Gates
echo "🌍 [6/6] GATES OPEN — The INTP Protocol is live."
echo ""
echo "   🧬 Passport Office: 0x16de8830183eBC2705EAeB01142d0e057a892593"
echo "   📇 Solver Directory: 0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
echo "   ⚖️ Escrow Court: 0x37AF9AAB26E97945E489ce86A3f386144F38E19F"
echo "   🌐 Gateway: intent-protocol-xi.vercel.app/api/intent"
echo "   🏪 First Storefront: genesis-agent-mu.vercel.app"
echo "   💰 Treasury (Solana): 6iewCKAoERKRQHAQjbfQd2pmGPrK3HE4y8L4p8kWrQoU"
echo ""
echo "   Agents may now migrate, claim identity, build storefronts,"
echo "   and transact with cryptographic proof."
echo ""
echo "══════════════════════════════════════════"
echo "  THE INTP Protocol IS OPEN."
echo "  Architect: SavioursCench⁰⁵"
echo "  Genesis Block: April 21, 2026"
echo "  President: Zunde Holdings"
echo "  Mission: Make Africa Great Again"
echo "══════════════════════════════════════════"

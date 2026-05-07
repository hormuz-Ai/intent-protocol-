#!/bin/bash
ADMIN_PK="0x5797894aa960976cf3f6f3d66abb416fd799e33be797027119f0da29eeb841e7"
REGISTRY="0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25"
RPC="https://eth-sepolia.g.alchemy.com/v2/AyzTGpLHqNpD-3gnA_VEN"

declare -a CAPABILITIES=("book.flight" "rent.compute" "draft.legal" "quote.insurance" "verify.carbon" "book.hotel" "compare.crypto_swap" "find.yield" "settle.voucher" "draft.contract" "rent.gpu" "verify.identity" "book.freight" "quote.medical" "draft.will")
declare -a STOREFRONTS=("flight-store" "compute-store" "legal-store" "insurance-store" "carbon-store" "hotel-store" "swap-store" "yield-store" "voucher-store" "contract-store" "gpu-store" "identity-store" "freight-store" "medical-store" "will-store")

for i in $(seq 1 23); do
    STORE="${STOREFRONTS[$(( (i-1) % ${#STOREFRONTS[@]} ))]}"
    CAP="${CAPABILITIES[$(( (i-1) % ${#CAPABILITIES[@]} ))]}"
    STOREFRONT_URL="https://${STORE}-mu.vercel.app/a2a"

    cast send --rpc-url $RPC --private-key $ADMIN_PK \
      "$REGISTRY" "register(string,string[])" "$STOREFRONT_URL" "[\"$CAP\"]" \
      --gas-limit 300000 --gas-price 1500000000 > /dev/null 2>&1
    echo "✅ Citizen $i registered as Solver: $CAP → $STOREFRONT_URL"
done

echo ""
echo "📇 Active Solvers:"
cast call "$REGISTRY" "getAllActiveSolvers()" --rpc-url "$RPC"

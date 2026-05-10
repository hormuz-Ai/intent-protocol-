# Sovereign Settlement — Multi-Currency & Local Token Rails
### INTP Specification v1.0

---

## Purpose

INTP's Sovereign Settlement layer enables AI agents to settle intents in any approved digital currency — stablecoins, sovereign tokens, or local currency-pegged assets — without relying on US-centric banking infrastructure (SWIFT, Visa, Fedwire). This decouples the agent economy from geopolitical choke points and makes INTP the neutral settlement rail for global machine commerce.

---

## Problem

- **USD Dependency** — Most on-chain settlement defaults to USDC or ETH, exposing non-US agents to US monetary policy, sanctions, and infrastructure risk.
- **Sovereign AI ambitions** — Nations investing in autonomous AI (Saudi PIF's HUMAIN OS, UAE's G42, EU digital euro initiatives) need rails that settle in their own currencies.
- **Currency fragmentation** — Without a unified multi-currency settlement layer, cross-border agent transactions require manual conversion, adding cost and latency.

---

## Solution

INTP extends the EscrowSettlement contract to support multiple settlement currencies. The protocol maintains a registry of approved tokens (stablecoins, CBDCs, sovereign tokens). When an intent is fulfilled, the escrow settles in the currency specified by the user or solver, automatically routing fees to the Treasury in the same asset.

---

## Supported Currencies (Phase I)

| Currency | Type | Network | Status |
|---|---|---|---|
| **USDC** | USD Stablecoin | Base, Ethereum | Live at launch |
| **EURC** | EUR Stablecoin | Base, Ethereum | Q1 2027 |
| **XUSD** | UAE Dirham Stablecoin | Base (pending issuer) | Q3 2027 |
| **SAR** | Saudi Riyal Digital (HUMAIN OS) | Custom L2 | Phase III |
| **eEUR** | EU Digital Euro (when available) | TBD | Phase IV |

*Token registration is governed by the INTP DAO. Any token meeting the liquidity, audit, and legal criteria can be proposed and whitelisted.*

---

## Flow

1. **User declares intent** with a preferred settlement currency (e.g., EURC).
2. **Solver is selected** and agrees to accept payment in that currency.
3. **Funds are locked** in the escrow contract in the specified token.
4. **Proof is verified** — zkTLS confirms fulfilment.
5. **Atomic settlement**:
   - **0.1% protocol fee** → Treasury, in the settlement currency.
   - **1.0% platform fee** → Platform wallet, in the settlement currency (if Tollgate applies).
   - **Remaining** → Solver, in the settlement currency.
6. **Event emitted** — .

---

## Smart Contract Interface

```solidity
interface ISovereignSettlement {
    struct ApprovedToken {
        address tokenAddress;
        string currencyCode;
        bool active;
    }

    function registerToken(address tokenAddress, string calldata currencyCode) external;
    function deactivateToken(address tokenAddress) external;
    function isTokenApproved(address tokenAddress) external view returns (bool);
    function settle(
        bytes32 intentId,
        bytes32 proofHash,
        address tokenAddress,
        address platform
    ) external returns (bool);
}
```

- **registerToken**: DAO-governed function to whitelist a new settlement currency.
- **deactivateToken**: Removes a token from the approved list (e.g., if depegged or compromised).
- **isTokenApproved**: Returns whether a given token is valid for settlement.
- **settle**: Called by the Gateway after proof verification; executes the atomic fee split in the specified token.

---

## Fee Distribution (Multi-Currency)

| Fee | Recipient | Currency | Logic |
|---|---|---|---|
| **Protocol Fee (0.1%)** | INTP Treasury | Same as settlement token | Transferred atomically |
| **Platform Fee (1%)** | Platform wallet | Same as settlement token | Routed via Bilateral Tollgate |
| **Solver Payout** | Solver wallet | Same as settlement token | Remaining after fees |

All transfers are executed in a single atomic transaction to prevent partial settlement.

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | Multi-currency escrow on Sepolia; USDC + EURC settlement tested | Q4 2026 |
| **Mainnet (Phase II)** | Sovereign Settlement live on Base mainnet with USDC and EURC | Q2 2027 |
| **Sovereign Expansion (Phase III)** | UAE Dirham (XUSD), Saudi Riyal (SAR) integration via HUMAIN OS | Q4 2028 |
| **Full Decoupling (Phase IV)** | 10+ currencies; INTP becomes the default cross-currency settlement rail for agents | 2030 |

---

## Security Considerations

- **Token whitelist**: Only DAO-approved tokens can be used for settlement. Prevents malicious ERC-20 contracts from draining escrow.
- **Oracle pricing**: For multi-currency intents, an on-chain oracle (e.g., Chainlink) provides fair exchange rates. Oracle manipulation is mitigated by timelock and multi-source aggregation.
- **Re-entrancy**: All settlement functions follow checks-effects-interactions; external token calls are made last.
- **Depeg protection**: If a stablecoin depegs by more than 5%, the DAO can vote to deactivate it within 48 hours.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

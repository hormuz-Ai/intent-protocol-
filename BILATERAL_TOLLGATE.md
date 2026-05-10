# Bilateral Tollgate — Automatic Platform Access Fee
### INTP Specification v1.0

---

## Purpose

The Bilateral Tollgate enables AI agents to access partner platforms (e.g., Amazon, Uber, Expedia) legitimately and automatically. Instead of scraping or violating Terms of Service, the INTP protocol negotiates a **1% access fee** on every agentic transaction and routes it to the platform. This turns platforms from gatekeepers into revenue partners.

---

## Problem

- **March 2026 CFAA ruling (Amazon v. Perplexity):** user permission alone does not constitute platform authorization. Agents that scrape without an API agreement are illegal.
- **Platforms lose revenue** blocking agents; they have no mechanism to charge them.
- **Agents need access** to real-world services to fulfill intents. Without a legal pathway, the agent economy stalls.

---

## Solution

INTP's Bilateral Tollgate smart contract automates the negotiation and payment of a 1% access fee, deducted from the solver's revenue and routed to the platform's designated wallet.

- **No API key required** – the agent accesses the platform via zkTLS, proving a legitimate session occurred.
- **No manual negotiation** – the fee percentage and payment terms are encoded on-chain and executed automatically.
- **Platform earns revenue** – every successful agentic transaction generates a fee for the platform.

---

## Flow

1. **Agent declares intent** (e.g., "Book flight to Nairobi").
2. **Solver is selected** via the INTP Registry.
3. **Solver executes the task** on the target platform (via official API or zkTLS browser session).
4. **zkTLS proof is generated**, confirming the platform's response and the final price.
5. **EscrowSettlement.sol verifies the proof** and calculates fees:
   - **0.1%** → INTP Treasury
   - **1.0%** → Platform wallet (Bilateral Tollgate)
   - **Remaining** → Solver
6. **Funds are released** simultaneously in a single atomic transaction.

---

## Smart Contract Interface

```solidity
interface IBilateralTollgate {
    struct Platform {
        address wallet;
        uint256 feeBps;      // default 100 (1%)
        bool active;
    }

    function registerPlatform(address wallet, uint256 feeBps) external;
    function updatePlatformFee(address wallet, uint256 feeBps) external;
    function getPlatformFee(address wallet) external view returns (uint256);
    function distributeFee(address platform, uint256 amount) external returns (bool);
}
```

- **registerPlatform**: called by the platform (or DAO) to enroll a wallet and set its fee.
- **updatePlatformFee**: adjusts the fee basis points (governed by DAO vote).
- **getPlatformFee**: returns the fee for a given platform wallet.
- **distributeFee**: internal function called by EscrowSettlement during settlement.

---

## Fee Parameters

| Parameter | Value | Governance |
|---|---|---|
| **Default Access Fee** | 1.0% (100 BPS) | DAO vote to adjust per platform |
| **Fee Recipient** | Platform's designated wallet | Set at registration |
| **Minimum Fee** | 0.1% (to prevent zero-fee gaming) | Hardcoded |
| **Maximum Fee** | 5.0% (to protect solvers) | Hardcoded |

---

## Integration with EscrowSettlement

The  contract is extended with a tollgate reference:

```solidity
IBilateralTollgate public tollgate;

function settle(bytes32 intentId, bytes32 proofHash, address platform) external {
    // ... verify proof ...
    uint256 total = e.totalAmount;
    uint256 protocolFee = (total * PROTOCOL_FEE_BPS) / BPS_DENOMINATOR;
    uint256 platformFee = (total * tollgate.getPlatformFee(platform)) / BPS_DENOMINATOR;
    uint256 solverPayout = total - protocolFee - platformFee;

    treasury.call{value: protocolFee}("");
    platform.call{value: platformFee}("");
    e.solver.call{value: solverPayout}("");
}
```

---

## Platform Onboarding

1. **Discovery** – INTP BD team contacts platform's partnerships or API team.
2. **Registration** – Platform provides a wallet address. DAO votes to approve and set the fee.
3. **Integration** – Platform whitelists INTP's zkTLS user-agent or provides an API endpoint.
4. **Go-Live** – First successful intent with tollgate fee distribution is published on BaseScan.

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | Tollgate smart contract on Sepolia; unit tests with mock platform | Q3 2026 |
| **Pilot** | First platform partner integrated; real 1% fee distributed on testnet | Q4 2026 |
| **Production (Phase II)** | Tollgate live on Base mainnet; 3+ platforms enrolled | Q2 2027 |
| **Scale (Phase III)** | 5+ major platforms (Amazon, Uber, Expedia, Airbnb, Shopify) | Q3 2028 |

---

## Security Considerations

- **Platform wallet validation:** Only DAO-approved wallets can receive tollgate fees; prevents impersonation.
- **Fee limits:** Hardcoded min/max prevent a malicious DAO from setting extortionate fees.
- **Atomic distribution:** All fee splits happen in a single transaction; no partial payments.
- **Upgrade path:** Tollgate contract is upgradeable via DAO vote + timelock.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

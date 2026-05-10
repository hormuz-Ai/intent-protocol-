# Procedural Memory — The Global Intent Brain
### INTP Specification v1.0

---

## Purpose

Procedural Memory stores the anonymized success path of every fulfilled intent — the solver used, the proof type, the settlement time, the fee breakdown — so that future intents can learn from history. The result is a self-improving protocol that gets faster, cheaper, and more reliable with every transaction.

---

## Problem

- Every intent is currently treated as a first-time event. The protocol does not learn which solver performed best for a given intent type, geography, or price range.
- Solvers must be rediscovered for each new intent, adding latency.
- There is no historical data to train AI routers or to show investors the protocol's improvement trajectory.

---

## Solution

After every successful settlement, the escrow contract emits an event containing the anonymized success path. An off-chain indexer stores this path in a decentralized vault (Walrus / Arweave). A query layer allows the Gateway to retrieve the best-performing solver for a given intent fingerprint without revealing any user data.

---

## Success Path Schema

```json
{
  "pathId": "0xabc123...",
  "intentFingerprint": "flight:JNB-NBO:economy:under500",
  "solverRegistryId": "0xsolver...",
  "category": "travel",
  "proofType": "zkTLS",
  "settlementTime": 4.2,
  "totalFee": 12.50,
  "protocolFee": 0.125,
  "platformFee": 1.25,
  "timestamp": 1715000000
}
```

- **pathId**: Unique hash of the success path.
- **intentFingerprint**: A generalized, anonymized representation of the intent (category + constraints).
- **solverRegistryId**: The on-chain solver that succeeded.
- **proofType**: The cryptographic proof used (zkTLS, on-chain data).
- **settlementTime**: Seconds from intent submission to proof verification.
- **totalFee**: The total cost to the user.
- **protocolFee**: The 0.1% routed to the Treasury.
- **platformFee**: The 1% platform access fee (if applicable).

---

## Flow

1. **Settlement** –  emits .
2. **Indexing** – A lightweight off-chain service (CIO Agent) picks up the event and writes the full success path to a decentralized vault.
3. **Storage** – Data is stored on Walrus (Sui-based) or Arweave, encrypted with a protocol key, accessible only to the Gateway.
4. **Query** – When a new intent arrives, the Gateway queries the Procedural Memory for the top 3 solvers matching the intent fingerprint.
5. **Routing** – The Gateway prioritizes solvers with the best historical performance for that fingerprint.

---

## Query Interface

```solidity
interface IProceduralMemory {
    function queryBestSolvers(
        string calldata intentFingerprint,
        uint256 limit
    ) external view returns (address[] memory solvers, uint256[] memory scores);

    function recordSuccess(
        bytes32 intentId,
        string calldata intentFingerprint,
        address solver,
        uint256 settlementTime,
        uint256 totalFee
    ) external;
}
```

- **queryBestSolvers**: Returns the top-performing solver addresses and their reliability scores for a given fingerprint.
- **recordSuccess**: Called by the escrow contract upon fulfilment to register a new success path.

---

## Integration with EscrowSettlement

```solidity
function verifyProof(bytes32 intentId, bytes32 proofHash) external {
    // ... existing verification ...
    emit Fulfilled(intentId, proofHash);

    // Record success path
    string memory fingerprint = _generateFingerprint(e.category, e.constraints);
    proceduralMemory.recordSuccess(intentId, fingerprint, e.solver, block.timestamp - e.createdAt, e.totalAmount);
}
```

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | Off-chain indexer + Walrus integration; query endpoint live on testnet Gateway | Q3 2026 |
| **Testnet** | Solver prioritization based on historical performance; 10k+ success paths indexed | Q4 2026 |
| **Mainnet (Phase II)** | Procedural Memory live on Base mainnet; routing engine uses historical data | Q2 2027 |
| **Global Brain (Phase III)** | External protocols query INTP's Procedural Memory via open API | Q4 2028 |

---

## Security Considerations

- **Anonymization**: Intent fingerprints never contain user addresses, names, or specific amounts. Only generalized categories and constraints are stored.
- **Encryption**: Success paths are encrypted with a protocol key managed by the DAO; only the Gateway can decrypt for queries.
- **Decentralized storage**: Walrus/Arweave ensures data persistence even if INTP's off-chain services are unavailable.
- **Query rate limiting**: Prevents scraping or denial-of-service on the memory vault.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

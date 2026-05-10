# Recursive Escrow — Multi-Agent Finality Settlement
### INTP Specification v1.0

---

## Purpose

The current EscrowSettlement contract handles single-agent settlement: one user, one solver, one proof. The agent economy increasingly involves multi-party workflows where multiple solvers must each deliver a component before the overall intent is fulfilled. Recursive Escrow extends the settlement layer to support **multi-agent finality** – funds are locked and only released when all required proofs are verified.

---

## Problem

- A single intent may require a chain of solvers (e.g., flight booking + hotel booking + insurance purchase).
- Partial fulfilment is not acceptable – if one solver fails, the entire intent must be refunded or reassigned.
- Current escrow logic has no concept of parent-child intents or dependency trees.

---

## Solution

Recursive Escrow introduces:

- **Intent Trees:** A parent intent can spawn child intents, each with its own solver, locked funds, and proof requirement.
- **Finality Conditions:** The parent escrow only releases funds when all child escrows reach  status.
- **Atomic Refund:** If any child fails, the entire tree can be unwound and funds returned to the user.

---

## Data Structures

```solidity
struct Escrow {
    address user;
    uint256 totalAmount;
    uint256 protocolFee;
    uint256 platformFee;
    Status status;
    bytes32[] childIntentIds;   // NEW: list of child intents
    uint256 requiredChildCount;  // NEW: how many children must succeed
    uint256 fulfilledChildCount; // NEW: running tally
}
```

---

## Flow

1. **Parent intent created** – User locks funds for a complex task (e.g., "plan my trip to Nairobi").
2. **Child intents spawned** – Gateway breaks the task into sub-intents: flight, hotel, insurance. Each child locks a portion of the total funds and is assigned a solver.
3. **Independent fulfilment** – Each child solver executes its task and submits a zkTLS proof.
4. **Child finality** – As each child is verified,  increments.
5. **Parent finality** – When , the parent escrow releases the remaining solver payouts.
6. **Failure handling** – If any child expires or is slashed, the entire tree can be refunded to the user.

---

## Smart Contract Interface

```solidity
interface IRecursiveEscrow {
    function createChildIntent(
        bytes32 parentIntentId,
        bytes32 childIntentId,
        address solver,
        uint256 amount,
        uint256 deadline
    ) external;

    function verifyChildProof(
        bytes32 parentIntentId,
        bytes32 childIntentId,
        bytes32 proofHash
    ) external;

    function refundTree(bytes32 parentIntentId) external;
}
```

- **createChildIntent**: Called by the Gateway to register a sub-task.
- **verifyChildProof**: Called when a child solver submits a valid zkTLS proof.
- **refundTree**: Called if a child fails; unwinds all locked funds back to the user.

---

## Fee Distribution

Fees are calculated at the parent level:

| Fee | Recipient | Calculation |
|---|---|---|
| **Protocol Fee** | INTP Treasury | 0.1% of total parent value |
| **Platform Fee** | Platform wallet (via Tollgate) | 1% of total parent value |
| **Solver Payouts** | Individual child solvers | Proportional to their locked amount, minus fees |

All fees are settled atomically when the parent intent reaches finality.

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | RecursiveEscrow.sol on Sepolia; 2-child intent demo | Q3 2026 |
| **Testnet** | Multi-solver intent with 3+ children; failure refund tested | Q4 2026 |
| **Mainnet** | Recursive Escrow live on Base mainnet | Q2 2027 |

---

## Security Considerations

- **Child limit:** Hardcoded maximum of 10 children per parent to prevent gas exhaustion.
- **Timeout enforcement:** Each child has its own deadline; if any expires, the entire tree can be refunded.
- **Re-entrancy:** All external calls (fee distribution, refunds) follow checks-effects-interactions pattern.
- **Upgrade path:** Recursive Escrow is deployed as a new contract; existing single-party escrow remains unchanged for backward compatibility.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

# Auto-Slashing Bonds — Solver Staking & Compensation
### INTP Specification v1.0

---

## Purpose

The Auto-Slashing Bonds mechanism requires every solver to stake INTP tokens (or approved stablecoins) before accepting intents. If the solver fails to deliver a valid zkTLS proof within the agreed deadline, the staked bond is automatically slashed and transferred to the user as compensation. This eliminates the need for manual dispute resolution and creates a self-insuring, trust-minimized solver network.

---

## Problem

- **Solver reliability** – An agent that commits to booking a flight but fails wastes the user’s time and blocks capital.
- **Dispute cost** – Manual arbitration is slow, expensive, and centralised.
- **User protection** – Users have no guarantee that a solver will perform as promised.

---

## Solution

Every solver must lock a bond proportional to the maximum value of the intents they wish to handle. A slashing contract monitors the fulfilment deadline. If no valid zkTLS proof is submitted by the deadline, the bond is automatically forfeited and sent to the user’s wallet. If the solver succeeds, the bond remains locked and can be withdrawn when the solver exits the network.

---

## Bond Parameters

| Parameter | Value | Governance |
|---|---|---|
| **Bond Ratio** | 1–10% of maximum intent value | Solver chooses within range |
| **Minimum Bond** | 1,000 INTP (or equivalent stablecoin) | DAO adjustable |
| **Slashing Penalty** | 100% of bond for the failed intent | Hardcoded |
| **Cooldown Period** | 7 days after last intent before bond can be withdrawn | DAO adjustable |
| **Dispute Window** | 48 hours for the solver to challenge a slash (via DAO) | Hardcoded |

---

## Flow

1. **Solver registers** – Calls  on the SlashingBonds contract, locking the required bond.
2. **Solver accepts intent** – The escrow contract records the solver’s bond ID and the fulfilment deadline.
3. **Fulfilment** – If the solver submits a valid zkTLS proof before the deadline, the bond remains untouched.
4. **Failure** – If the deadline passes without a valid proof, anyone can call . The bond is automatically transferred to the user.
5. **Withdrawal** – After a cooldown period with no active intents, the solver may call  to retrieve their remaining bond.

---

## Smart Contract Interface

```solidity
interface ISlashingBonds {
    struct Bond {
        address solver;
        uint256 amount;
        uint256 lockedUntil;
        uint256 activeIntents;
    }

    function stake(uint256 amount) external returns (bytes32 bondId);
    function slash(bytes32 intentId, bytes32 bondId) external returns (bool);
    function withdrawStake(bytes32 bondId) external returns (bool);
    function getBond(bytes32 bondId) external view returns (Bond memory);
}
```

- **stake**: Locks tokens from the solver’s wallet and issues a bond.
- **slash**: Called by the escrow contract (or any watcher) when an intent expires unfulfilled. Transfers the bond to the user.
- **withdrawStake**: Returns unlocked tokens to the solver after cooldown.
- **getBond**: Returns current bond details.

---

## Integration with EscrowSettlement

```solidity
function verifyProof(bytes32 intentId, bytes32 proofHash) external {
    Escrow storage e = escrows[intentId];
    require(e.status == Status.Pending, "Not pending");
    require(block.timestamp <= e.deadline, "Expired");
    e.status = Status.Fulfilled;
    e.proofHash = proofHash;
    // Bond is safe; no slashing
}

function slash(bytes32 intentId) external {
    Escrow storage e = escrows[intentId];
    require(e.status == Status.Pending, "Not pending");
    require(block.timestamp >= e.deadline, "Not expired");
    e.status = Status.Slashed;
    // Trigger bond slashing
    slashingBonds.slash(intentId, e.bondId);
    // Refund user from bond + locked amount
    (bool sent, ) = e.user.call{value: e.lockedAmount}("");
    require(sent, "Refund failed");
    emit Slashed(intentId, e.solver);
}
```

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | SlashingBonds.sol on Sepolia; unit tests with mock escrow | Q3 2026 |
| **Testnet** | Live bond staking and slashing with real solvers | Q4 2026 |
| **Mainnet (Phase II)** | Auto-Slashing Bonds mandatory for all high-value intents on Base mainnet | Q2 2027 |
| **Scale (Phase III)** | Bond pool exceeds 00M; used by insurers for underwriting | Q4 2028 |

---

## Security Considerations

- **Bond custody:** The slashing contract holds all staked tokens. Audited by a top-tier firm before mainnet.
- **Re-entrancy protection:** Slashing and withdrawal functions use re-entrancy guards.
- **Griefing protection:** A 48-hour dispute window allows a solver to challenge a wrongful slash via DAO vote.
- **Minimum bond:** Prevents dust attacks where solvers stake negligible amounts and walk away.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

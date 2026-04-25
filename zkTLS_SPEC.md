# INTP Settlement Oracle — zkTLS Specification v1.0

## Problem
A solver can claim it booked a flight for $350. The gateway has no
cryptographic proof that the booking actually happened. The current
system relies on trust. In a permissionless network, trust is
unacceptable.

## Solution: zkTLS
Zero‑Knowledge Transport Layer Security (zkTLS) allows a solver to
cryptographically prove it received a specific response from an
external API (e.g., an airline’s booking endpoint) via a legitimate
TLS session — without revealing the user’s credentials or the
solver’s API keys.

As of early 2026, zkTLS infrastructure is deployed across 20+
projects on Arbitrum, Sui, Polygon, and Solana. INTP will integrate
a zkTLS oracle (Brevis co‑processor or Reclaim Protocol fork) to
verify fulfillment proofs on‑chain before any fee is collected.

## Architecture
1. Solver calls external API (e.g., AviationStack) via standard TLS.
2. Solver generates a ZK proof that the TLS session was authentic,
   the response was unmodified, and the price matches the claimed
   value.
3. Proof is submitted to the INTP Settlement Oracle (smart contract).
4. Oracle verifies the proof on‑chain.
5. If valid → protocol fee (0.1%) is released. If invalid → solver
   is slashed.

## Implementation Roadmap
- Q2 2026 (current): Specification published. Solver API integration
  standardized.
- Q3 2026: zkTLS oracle deployed on Sepolia testnet. Reference
  implementation with Brevis co‑processor.
- Q4 2026: Oracle audited. Mainnet deployment.

## Security
- Post‑quantum readiness: zkTLS proofs are hash‑based, making them
  resistant to quantum attacks when combined with SPHINCS+
  signatures.
- Formal verification: Oracle smart contract verified with
  SMTChecker.

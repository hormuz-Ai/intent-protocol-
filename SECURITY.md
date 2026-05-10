# INTP Security Framework
### Threat Model, Audit Roadmap & Bug Bounty Program

---

## 1. Security Principles

INTP is a settlement layer for autonomous AI agents. Compromise is not an option. Every security decision follows three principles:

- **Defence in Depth** – No single control point. The protocol is secured by cryptography, economic incentives, and governance, not trust.
- **Quantum‑Proof by Default** – All long‑term treasury actions require post‑quantum signatures (SPHINCS+, FIPS 205).
- **Transparency** – Every contract is verified on‑chain. Every vulnerability report is acknowledged publicly. Every fix is published with a post‑mortem.

---

## 2. Threat Model

| Threat | Mitigation | Status |
|---|---|---|
| **Smart Contract Exploit** | External audit (pre‑mainnet) + formal verification (SMTChecker, Kani) + timelocked upgrades | Audit planned Q3 2026 |
| **Oracle Manipulation** | zkTLS cryptographic proof required for settlement; no trusted data sources | Live on Sepolia |
| **Sybil Solvers** | ERC‑8004 hardware attestation (NVIDIA Vera Rubin TEE) + INTP staking requirement | ERC‑8004 migration Q1 2027 |
| **Private Key Compromise** | 3‑of‑5 Safe multisig for Treasury; no single signer can move funds | Safe deployed on Base |
| **Quantum Attack** | SPHINCS+ signatures for all administrative treasury operations from Q3 2026 | Integration planned |
| **Denial of Service** | Decentralised hosting (IPFS/ICP) in Phase III; rate limiting on gateway APIs | Phase III |
| **Governance Attack** | 10% quorum requirement + 48‑hour timelock on all proposals | Activated with DAO |

---

## 3. Audit Roadmap

| Audit | Scope | Timeline | Auditor |
|---|---|---|---|
| **Pre‑Mainnet Security Review** | EscrowSettlement.sol, SolverRegistry.sol, AgentPassport.sol | Q3 2026 | To be selected (top‑tier firm) |
| **zkTLS Oracle Audit** | Reclaim Protocol integration, on‑chain proof verification | Q4 2026 | Specialist ZK auditor |
| **Formal Verification** | EscrowSettlement.sol core logic (SMTChecker, Kani) | Q1 2027 | Internal + external review |
| **Governance & Treasury Audit** | Safe multisig configuration, DAO voting contracts, timelock | Q2 2027 | To be selected |
| **Annual Re‑Audit** | All contracts, new features, cross‑chain bridges | Annually | Rotating auditors |

---

## 4. Bug Bounty Program

INTP operates a public bug bounty program funded by the Treasury.

| Parameter | Value |
|---|---|
| **Platform** | Immunefi (or equivalent) |
| **Rewards** | Up to $500,000 for critical vulnerabilities (Treasury theft) |
| **Scope** | All smart contracts, the zkTLS oracle, the Gateway API, and the Safe multisig configuration |
| **Disclosure** | 90‑day responsible disclosure window; all validated reports published with a post‑mortem |
| **Funding** | Allocated by DAO vote from the Treasury |

---

## 5. Post‑Quantum Readiness

All administrative treasury transactions will require **SPHINCS+ (FIPS 205)** signatures starting Q3 2026. SPHINCS+ is a stateless hash‑based signature scheme standardised by NIST that provides security against both classical and quantum adversaries. The protocol's key rotation and upgrade path ensures that if a vulnerability in SPHINCS+ or any other signature scheme is discovered, the multisig can rotate to a new scheme via DAO vote and timelocked execution.

---

## 6. Incident Response

1. **Detection** – On‑chain monitoring via the CFO Agent and third‑party services (e.g., Forta, OpenZeppelin Defender).
2. **Containment** – Emergency pause functionality (governed by multisig until DAO assumes full control).
3. **Resolution** – All fixes submitted as DAO proposals, publicly discussed, and timelocked.
4. **Post‑Mortem** – Every incident published with root cause, impact assessment, and remediation steps.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

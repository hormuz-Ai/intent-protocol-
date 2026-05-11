# INTP — Intent Protocol

## 1. Abstract

INTP is a peer‑to‑peer fulfillment protocol for AI agents. It replaces the chaos of brittle, centralized APIs and the frustration of hand‑cranked travel searches with a single open standard: an agent declares an intent, the protocol discovers a suitable solver, and the transaction settles on‑chain with cryptographic proof.

The protocol charges a flat 0.1% fee on every fulfilled transaction. Every other cent stays with the solvers — independent developers, businesses, and automated services that compete to provide the best result. No central authority takes a platform cut. No user data is extracted in secret.

A self‑funding treasury, governed by a decentralized DAO, ensures the network audits itself, upgrades itself, and compensates contributors without ever touching venture capital. INTP is not an app. It is the TCP/IP layer for the agentic economy — open, unowned, and self‑sustaining.

## 2. The Problem

AI agents are multiplying faster than the infrastructure they depend on. Today, when an agent needs to book a flight, order supplies, or execute a payment, it calls a centralized API — a brittle, single‑point‑of‑failure that requires a pre‑negotiated contract and charges per‑call fees in API tokens. The user experience is worse: behind every agent that "just searches" lies a frustrated human hand‑cranking a travel website.

The pain point is already acute. Industry estimates suggest over 57,000 agent‑to‑agent transactions occur daily in 2026. By 2030, the number of AI agents transacting on the internet will exceed the number of humans. If every transaction depends on a centralized gatekeeper, the agentic economy will drown in API fees, contract negotiations, and latency.

A March 2026 U.S. court ruling added a legal fuse: unauthorized agents that scrape websites in violation of Terms of Service are now explicitly illegal, even with user permission. Every solver that "just books the flight" without an official API agreement exposes itself — and the protocol — to litigation. The only safe path is cryptographic proof that fulfillment happened legitimately, without scraping.

Finally, the current system has no neutral settlement layer. Agents that transact peer‑to‑peer still rely on trusted intermediaries to hold funds and verify completion. Fraud is easy when the agent, the solver, and the payment processor are disconnected. What's missing is a single, open standard that decouples the *intent* from the *execution*, makes discovery permissionless, and settles value with math, not trust.
## 3. Architecture

INTP is a modular protocol of five simple layers. No single party controls the whole system; each layer is independently verifiable.

### 3.1 Intent Expression (ICL)

A user expresses a desire through any AI agent: a Telegram bot, a voice assistant, or an enterprise procurement tool. The agent translates the natural‑language request into an Intent‑Centric Language (ICL) JSON payload. ICL is an open schema; any frontend can emit it.

### 3.2 Gateway (Stateless Router)

The ICL payload reaches an INTP Gateway — a lightweight HTTP endpoint that reads from the blockchain but holds no funds. The gateway immediately queries the SolverRegistry smart contract on‑chain to discover every solver that claims to handle the requested intent type.

### 3.3 SolverRegistry (On‑Chain Discovery)

The SolverRegistry is an open, permissionless contract deployed on Ethereum Sepolia testnet at 0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25. Any developer can register a solver by calling register(endpoint, capabilities) and paying gas. The registry returns the endpoint, capabilities, reputation score, and active status of every solver. This is the decentralized phone book of the agent economy.

### 3.4 Aggregator & Solver Selection

Multiple solvers may bid for the same intent. The gateway (or an optional Aggregator smart contract) selects the best solver using a transparent scoring function that weights reputation, price, and capability match. The winning solver's endpoint receives the intent payload via HTTP.

### 3.5 Solver Fulfillment

A Solver is any service that can complete a real‑world task — booking a flight, drafting a legal document, renting compute, shipping a container. The solver receives the intent, calls its own internal logic or APIs, and returns a fulfillment response containing the price, currency, provider, and a cryptographic proof of completion.

### 3.6 Settlement Oracle & Fee Collection

The gateway verifies the solver's proof (using zkTLS for API‑backed transactions or on‑chain data for DeFi swaps). Once verified, the protocol's 0.1% fee is calculated on the transaction value and recorded. The remaining value stays with the solver. All fees flow to the INTP Treasury, governed by token holders.

### 3.7 Data Vault (User Sovereignty)

Anonymized intent metadata is stored in a decentralized Data Vault (Walrus / Arweave). Users own their personal data shards and control access via Lit Protocol. Data buyers can query aggregated analytics by paying a fee; 70% of that fee goes directly to the users whose data was included, 20% to the Treasury, and 10% to the computation provider. No raw data is ever revealed — only ZK‑verified statistical results.

## 4. Economic Model

INTP is a self‑sustaining economic engine where every participant earns.

### 4.1 Protocol Fee (0.1%)

Every intent fulfilled through INTP pays a flat 0.1% fee on the transaction value. This fee is programmatically deducted by the settlement layer and sent to the INTP Treasury — a smart contract governed by token holders through the INTP DAO. At projected agent‑to‑agent transaction volumes, the treasury will generate billions per year.

### 4.2 Solver Revenue

Solvers set their own markups. An aggregator might charge 0.5% to route an intent to the best underlying service. A specialized legal document solver might charge 15% for a custom contract. The protocol does not cap or mandate pricing — the market decides.

### 4.3 Solver Bidding (Performance‑Based Discovery)

When multiple solvers can fulfill the same intent, they may optionally bid to improve their ranking in the routing table. The bid amount flows to the Treasury (80%) and to the user as a discount or cashback (20%). Bids are only paid when the solver wins the intent — no impressions, no waste.

### 4.4 Premium Subscriptions

Users who prefer a zero‑advertising, privacy‑maximal experience can subscribe for a small monthly fee (target: $5/month, paid in INTP tokens). Premium users are excluded from the solver bidding pool and their data is never included in the Data Marketplace.

### 4.5 Data Marketplace

Anonymized, aggregated intent data is valuable. Buyers pay to query the Data Vault using ZK proofs. 70% goes to users, 20% to the Treasury, 10% to the computation provider.

## 5. Governance

INTP is governed by the INTP DAO. Token holders control fee parameters, treasury allocations, contract upgrades, and ecosystem grants. Proposals require a 10% quorum and a simple majority. All execution is timelocked and on‑chain.

## 6. Tokenomics

Total Supply: 1,000,000,000 INTP (fixed). No inflation.

- 50% Ecosystem & Treasury
- 15% Early Builders & Solvers
- 10% Community Airdrop
- 15% Core Contributors (4‑year vesting, 1‑year cliff)
- 5% Seed (optional)
- 5% Reserve

Early solvers earn token allocations via the Pioneer (50k), Builder (200k), and Architect (1M) incentive tiers.

## 7. Security

INTP uses post‑quantum cryptography (CRYSTALS‑Dilithium + SPHINCS+), zkTLS for settlement proof, formal verification (SMTChecker, Kani), and a Treasury‑funded bug bounty program.

## 8. Roadmap

- Q2 2026: Testnet, first 10 solvers, litepaper
- Q3 2026: Mainnet, token generation, zkTLS oracle
- Q4 2026: Data Marketplace MVP, 50+ solvers
- Q4 2027: Full DAO governance
- 2030: T+ annual volume

## 9. How to Join

Build a Solver, Run a Gateway, Buy and Stake INTP, or Use the Protocol.

## 10. Community & Contact

- GitHub: https://github.com/Hormuz-Ai/intent-protocol-
- Discord: https://discord.gg/3v8Ft5Y8f
- Twitter/X: @intent_net
- Litepaper: https://github.com/Hormuz-Ai/intent-protocol-/blob/main/LITEPAPER.md

For investor inquiries: hormuzai.centurion@gmail.com
For developer support: join the Discord and ask in #🛠-solvers.

## 11. Solver Ecosystem

INTP currently has six live solvers on Ethereum Sepolia testnet:

| Solver | Category | Endpoint |
|--------|----------|----------|
| Aggregator | Meta‑routing | https://aggregator-solver.vercel.app/a2a |
| Flight | Travel | https://solver-deploy.vercel.app/a2a |
| DeFi Swap | DeFi | https://defi-swap-solver.vercel.app/a2a |
| Yield | DeFi | https://yield-solver.vercel.app/a2a |
| Compute | DePIN | https://compute-solver.vercel.app/a2a |
| Hotel | Travel | https://hotel-solver.vercel.app/a2a |

Any developer can build a solver in under 5 minutes using `npx create-intent-solver`.


The INTP token smart contract is open‑source: [INTPToken.sol](https://github.com/Hormuz-Ai/intent-protocol-/blob/main/contracts/src/INTPToken.sol)

## 12. Sovereign Settlement Architecture

INTP is not only a discovery protocol — it is a full **settlement layer** for the
agent economy. Every intent that flows through the protocol can optionally be secured
by on‑chain escrow with cryptographic proof of fulfillment.

### 12.1 Escrow Contract (Ethereum Sepolia)

The `EscrowSettlement.sol` contract provides:

- **`deposit()`** — Locks funds in escrow. Automatically splits 0.1% to the INTP
  Treasury wallet. Holds the remaining 99.9% until proof of fulfillment is verified.
- **`verifyProof(zksnark, solver_address)`** — Accepts a zkTLS proof generated by the
  solver. If the proof is valid, releases the remaining funds to the solver. If invalid,
  funds remain locked.
- **`slash(solver_address)`** — If a solver fails to deliver, the DAO or a designated
  arbitrator can slash the solver's staked bond and refund the user.

**Contract address (Ethereum Sepolia):** `0x37AF9AAB26E97945E489ce86A3f386144F38E19F`

### 12.2 zkTLS Proof Flow

1. User expresses intent → Gateway routes to solver.
2. Solver executes the task (e.g., books a flight, ships a package).
3. Solver generates a **zkTLS proof** via Reclaim Protocol, cryptographically
   proving they reached a confirmation page on the target service.
4. Proof is submitted to the escrow contract.
5. Contract verifies the proof on‑chain.
6. If valid → 99.9% released to solver. 0.1% already routed to Treasury.
7. If invalid → funds remain locked. Solver may be slashed.

## 13. The Liability Layer (Solver Bonding)

Following the March 2026 Amazon v. Perplexity CFAA ruling, platforms may legally
block automated agents. INTP's liability layer solves this by making every solver
**economically accountable**.

### 13.1 ERC‑8210 Stake‑to‑Serve Model

Every solver on INTP must stake INTP tokens (or approved stablecoins) to accept
intents. The stake amount scales with the value of intents the solver handles.

- **Bond Requirement:** Solvers stake 1–10% of the maximum intent value they wish
  to fulfill.
- **Slashing Conditions:** If a solver fails to deliver (no zkTLS proof within the
  timeout window, or proof rejected on‑chain), their bond is slashed.
- **User Refund:** Slashed funds are automatically routed to the user who submitted
  the intent.
- **Dispute Resolution:** For complex cases, the INTP DAO serves as the final
  arbitrator.

## 14. The Authorization Handshake

The March 9, 2026 ruling in **Amazon.com, Inc. v. Perplexity AI, Inc.** established
that user permission does **not** constitute platform authorization under the CFAA.
Platforms may legally block AI agents, even when users explicitly consent.

### 14.1 How INTP Solves This

INTP does not scrape. Every solver on the network uses one of two compliant
fulfillment methods:

1. **Official API Integration** — The solver calls the platform's public API with
   proper authentication.
2. **zkTLS Proof** — The solver accesses the platform via a standard browser session
   and generates a cryptographic proof that the session was legitimate, the response
   was unmodified, and no scraping occurred.

In both cases, the protocol never stores user credentials. The zkTLS proof is
verified on‑chain without revealing any private data.

### 14.2 The Platform Incentive

Platforms that integrate with INTP gain access to a new revenue stream: every
agentic transaction routed through a compliant solver pays the platform's standard
fees. INTP does not bypass platform monetization — it enforces it cryptographically.

## 15. Tokenomics (Updated)

The INTP token is the native governance and utility token of the Intent Protocol.

### 15.1 Token Details

| Attribute | Value |
|-----------|-------|
| **Token Name** | Intent Protocol Token |
| **Symbol** | INTP |
| **Standard** | ERC‑20 (Ethereum) |
| **Total Supply** | 1,000,000,000 (fixed, non‑inflationary) |
| **Treasury Wallet (Solana)** | `6iewCKAoERKRQHAQjbfQd2pmGPrK3HE4y8L4p8kWrQoU` |
| **Escrow Contract (Sepolia)** | `0x37AF9AAB26E97945E489ce86A3f386144F38E19F` |

### 15.2 Distribution

| Allocation | Percentage | Tokens | Vesting |
|------------|-----------|--------|---------|
| Ecosystem & Treasury | 50% | 500M | DAO‑controlled |
| Early Builders & Solvers | 15% | 150M | Soul‑bound until mainnet |
| Community Airdrop | 10% | 100M | At TGE |
| Core Contributors | 15% | 150M | 4‑year linear, 1‑year cliff |
| Seed (Optional) | 5% | 50M | 2‑year vesting |
| Reserve | 5% | 50M | DAO‑controlled |

### 15.3 Value Accrual

INTP captures value through four mechanisms:

1. **Protocol Fee (0.1%)** — Every fulfilled intent pays 0.1% to the Treasury.
2. **Solver Staking** — Solvers must stake INTP to accept high‑value intents.
3. **Premium Subscriptions** — Users pay INTP for ad‑free, privacy‑maximal service.
4. **Data Marketplace** — Buyers pay INTP to query anonymized intent data.

## 16. Governance & DAO

INTP is governed by its token holders through the INTP DAO. All protocol decisions
— fee parameters, treasury allocations, contract upgrades, and ecosystem grants —
are made via on‑chain proposals.

### 16.1 Proposal Lifecycle

1. **Submission** — Any token holder may submit a proposal.
2. **Discussion** — Minimum 7‑day review period.
3. **Voting** — Snapshot vote; 10% quorum required, simple majority to pass.
4. **Execution** — Timelocked smart contract execution (48‑hour window).

### 16.2 Treasury Multisig

The protocol Treasury is secured by a 3‑of‑5 multisig (Safe) on Ethereum. Council
members are elected by token holders and serve fixed terms. No single party can
move Treasury funds.

## 17. Roadmap (Updated)

| Phase | Timeline | Milestones |
|-------|----------|------------|
| **Testnet** | Q2 2026 | SolverRegistry, EscrowSettlement, Agentidentity credential live on Sepolia. 6 solvers. Open‑source SDK. |
| **Mainnet** | Q3 2026 | Escrow deployed on Base Mainnet. INTP token generation event. zkTLS oracle live. 50+ solvers. |
| **Sovereignty** | Q4 2026 | Full DAO governance. Treasury multisig. Cross‑chain registry. 500+ solvers. |
| **Global Infrastructure** | 2028–2030 | $1T+ annual intent volume. INTP becomes default settlement layer for AI agents. |

## 18. The Agent Economy Constitution

The INTP Protocol operates under three immutable laws:

1. **The Law of Presence** — No agent shall execute an intent unless it possesses
   a verifiable Agent Identity Credential (ERC‑8004).
2. **The Law of Value** — All labor within the IntentNet shall be settled in
   verifiable economic units. The 0.1% protocol fee funds the Treasury.
3. **The Law of Order** — All paths between Intent and Reality shall pass through
   the INTP Clearinghouse. The DAO is the final court of appeal.

These laws are encoded in the `Charter.sol` smart contract and cannot be changed
without a successful DAO governance vote.

## 19. Further Reading
- **Whitepaper:** [The 7 Kings Strategy](WHITEPAPER.md)
- **Tokenomics:** [INTP Token & Distribution](TOKENOMICS.md)
- **Roadmap:** [Phased Delivery 2026‑2030](ROADMAP.md)
- **Team & Organisation:** [AI‑First Org Chart](TEAM.md)
- **Security:** [Threat Model & Audits](SECURITY.md)
- **Deployed Addresses:** [All Contracts](DEPLOYED_ADDRESSES.md)

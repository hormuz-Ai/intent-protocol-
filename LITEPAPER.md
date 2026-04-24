# INTP — Intent Protocol

## 1. Abstract

INTP is a peer‑to‑peer fulfillment protocol for AI agents. It replaces the chaos of
brittle, centralized APIs and the frustration of hand‑cranked travel searches with a
single open standard: an agent declares an intent, the protocol discovers a suitable
solver, and the transaction settles on‑chain with cryptographic proof.

The protocol charges a flat 0.1% fee on every fulfilled transaction. Every other cent
stays with the solvers — independent developers, businesses, and automated services that
compete to provide the best result. No central authority takes a platform cut. No user
data is extracted in secret.

A self‑funding treasury, governed by a decentralized DAO, ensures the network audits
itself, upgrades itself, and compensates contributors without ever touching venture
capital. INTP is not an app. It is the TCP/IP layer for the agentic economy — open,
unowned, and self‑sustaining.

## 2. The Problem

AI agents are multiplying faster than the infrastructure they depend on. Today, when an
agent needs to book a flight, order supplies, or execute a payment, it calls a centralized
API — a brittle, single‑point‑of‑failure that requires a pre‑negotiated contract and
charges per‑call fees in API tokens. The user experience is worse: behind every agent that
"just searches" lies a frustrated human hand‑cranking a travel website.

The pain point is already acute. Industry estimates suggest over 57,000 agent‑to‑agent
transactions occur daily in 2026. By 2030, the number of AI agents transacting on the
internet will exceed the number of humans. If every transaction depends on a centralized
gatekeeper, the agentic economy will drown in API fees, contract negotiations, and
latency.

A March 2026 U.S. court ruling added a legal fuse: unauthorized agents that scrape
websites in violation of Terms of Service are now explicitly illegal, even with user
permission. Every solver that "just books the flight" without an official API agreement
exposes itself — and the protocol — to litigation. The only safe path is cryptographic
proof that fulfillment happened legitimately, without scraping.

Finally, the current system has no neutral settlement layer. Agents that transact
peer‑to‑peer still rely on trusted intermediaries to hold funds and verify completion.
Fraud is easy when the agent, the solver, and the payment processor are disconnected.
What's missing is a single, open standard that decouples the *intent* from the *execution*,
makes discovery permissionless, and settles value with math, not trust.

## 3. Architecture

INTP is a modular protocol of five simple layers. No single party controls the whole
system; each layer is independently verifiable.

### 3.1 Intent Expression (ICL)

A user expresses a desire through any AI agent: a Telegram bot, a voice assistant, or an
enterprise procurement tool. The agent translates the natural‑language request into an
**Intent‑Centric Language (ICL)** JSON payload. ICL is an open schema; any frontend can
emit it.

### 3.2 Gateway (Stateless Router)

The ICL payload reaches an INTP **Gateway** — a lightweight HTTP endpoint that reads
from the blockchain but holds no funds. The gateway immediately queries the
**SolverRegistry** smart contract on‑chain to discover every solver that claims to handle
the requested intent type.

### 3.3 SolverRegistry (On‑Chain Discovery)

The SolverRegistry is an open, permissionless contract deployed on Ethereum Sepolia
testnet at `0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25`. Any developer can register
a solver by calling `register(endpoint, capabilities)` and paying gas. The registry
returns the endpoint, capabilities, reputation score, and active status of every solver.
This is the decentralized "phone book" of the agent economy.

### 3.4 Aggregator & Solver Selection

Multiple solvers may bid for the same intent. The gateway (or an optional **Aggregator**
smart contract) selects the best solver using a transparent scoring function that
weights reputation, price, and capability match. The winning solver's endpoint receives
the intent payload via HTTP.

### 3.5 Solver Fulfillment

A **Solver** is any service that can complete a real‑world task — booking a flight,
drafting a legal document, renting compute, shipping a container. The solver receives the
intent, calls its own internal logic or APIs, and returns a fulfillment response
containing the price, currency, provider, and a cryptographic proof of completion.

### 3.6 Settlement Oracle & Fee Collection

The gateway verifies the solver's proof (using **zkTLS** for API‑backed transactions
or on‑chain data for DeFi swaps). Once verified, the protocol's 0.1% fee is calculated
on the transaction value and recorded. The remaining value stays with the solver.
All fees flow to the INTP Treasury, governed by token holders.

### 3.7 Data Vault (User Sovereignty)

Anonymized intent metadata is stored in a decentralized **Data Vault** (Walrus / Arweave).
Users own their personal data shards and control access via Lit Protocol. Data buyers
can query aggregated analytics by paying a fee; 70% of that fee goes directly to the users
whose data was included, 20% to the Treasury, and 10% to the computation provider. No raw
data is ever revealed — only ZK‑verified statistical results.

## 4. Economic Model

INTP is not a charity. It is a self‑sustaining economic engine where every participant
earns.

### 4.1 Protocol Fee (0.1%)

Every intent fulfilled through INTP pays a flat 0.1% fee on the transaction value.
This fee is programmatically deducted by the settlement layer and sent to the
**INTP Treasury** — a smart contract governed by token holders through the INTP DAO.
At $4.2 trillion in projected annual agent‑to‑agent transaction volume by 2030, the
treasury would generate $4.2 billion per year.

### 4.2 Solver Revenue

Solvers set their own markups. An aggregator might charge 0.5% to route an intent to
the best underlying service. A specialized legal document solver might charge 15% for
a custom contract. A commodity flight solver might compete on volume at 1%. The
protocol does not cap or mandate pricing — the market decides.

### 4.3 Solver Bidding (Performance‑Based Discovery)

When multiple solvers can fulfill the same intent, they may optionally bid to improve
their ranking in the routing table. The bid amount flows to the Treasury (80%) and to
the user as a discount or cashback (20%). Bids are only paid when the solver wins the
intent — no impressions, no waste. This is a fundamentally more efficient model than
Google's cost‑per‑click advertising.

### 4.4 Premium Subscriptions

Users who prefer a zero‑advertising, privacy‑maximal experience can subscribe for a
small monthly fee (target: $5, paid in INTP tokens). Premium users are excluded from
the solver bidding pool, meaning their results are purely reputation‑ and price‑based.
Their data is never included in the Data Marketplace. Subscription revenue goes to the
Treasury.

### 4.5 Data Marketplace

Intent metadata — anonymized, aggregated, and cryptographically verified — is the raw
material of the new internet economy. INTP stores this data in a decentralized Data
Vault (Walrus / Arweave) controlled by user‑owned access keys (Lit Protocol).

A buyer (e.g., an airline forecasting demand) submits a query and pays a fee.
A Zero‑Knowledge computation engine proves the query was executed correctly on real
data without revealing any individual record. The fee is distributed:

- **70% to users** whose data was included in the query
- **20% to the INTP Treasury**
- **10% to the node that performed the ZK computation**

Users are no longer the product. They are the beneficiaries.

## 5. Governance

INTP is governed by its users, not by a corporation. All protocol decisions — fee
parameters, treasury allocations, contract upgrades, and ecosystem grants — are made
by the **INTP DAO**, a decentralized autonomous organization where voting power is
proportional to INTP token holdings.

### 5.1 Proposal Lifecycle

1. **Submission**: Any token holder may submit a formal proposal on‑chain.
2. **Discussion**: A mandatory review period (minimum 7 days) allows the community to
   debate the proposal before voting begins.
3. **Voting**: A snapshot vote of INTP balances determines the outcome. Proposals
   require a quorum of 10% of circulating supply and a simple majority to pass.
4. **Execution**: Passed proposals are executed automatically by timelocked smart
   contracts, giving the community a final window to exit if they disagree.

### 5.2 Scope of Governance

The DAO controls:
- The protocol fee rate (initially 0.1%)
- Treasury fund allocation (audits, bounties, grants, staking rewards)
- Smart contract upgrades and integrations (e.g., new ZK proof systems)
- Slashing conditions for malicious solvers
- Data Marketplace fee splits

The DAO does **not** control individual solvers, user data, or intent content. These are
cryptographically protected and outside governance scope.

### 5.3 Transition to Full Decentralization

INTP follows a proven decentralization roadmap:

| Phase | Timeline | Governance Model |
|-------|----------|------------------|
| **Testnet** | Q2 2026 | Core contributors guide protocol; community input via forum |
| **Mainnet Launch** | Q3 2026 | INTP token distributed; DAO proposals begin; core team retains emergency pause |
| **Full DAO** | Q4 2027 | Emergency pause removed; all parameter changes exclusively via on‑chain vote |

## 6. Tokenomics

The INTP token is the native governance and utility token of the Intent Protocol.
It represents membership in the DAO, a claim on treasury revenue, and the primary
medium of exchange for solver bidding, premium subscriptions, and data marketplace
access.

### 6.1 Value Accrual

INTP captures value through three mechanisms:

- **Treasury Revenue Share**: The 0.1% protocol fee accumulates in the INTP Treasury,
  which the DAO may allocate to staking rewards, token buybacks, or strategic reserves.
- **Governance Control**: Controlling the parameters of a network that processes billions
  in transaction volume is intrinsically valuable. Token holders determine fee rates,
  treasury spending, and protocol upgrades.
- **Utility Demand**: Solvers must hold INTP to bid for routing priority. Premium users
  must hold INTP to subscribe. Data buyers must hold INTP to query the marketplace.
  This creates organic, non‑speculative demand.

For developer support: join the Discord and ask in #🛠-solvers.

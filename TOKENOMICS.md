# INTP Tokenomics
### Native Utility & Governance Token of the Intent Protocol

---

## 1. Token Details

| Attribute | Value |
|---|---|
| **Token Name** | Intent Protocol Token |
| **Symbol** | INTP |
| **Standard** | ERC‑20 (Ethereum / Base) |
| **Total Supply** | 1,000,000,000 (1 billion) |
| **Inflation** | Zero (fixed supply) |
| **Decimals** | 18 |

---

## 2. Distribution

| Allocation | Percentage | Tokens | Vesting |
|---|---|---|---|
| Ecosystem & Treasury | 50% | 500,000,000 | DAO‑controlled, released via governance votes |
| Early Builders & Solvers | 15% | 150,000,000 | Soul‑bound until mainnet, then 2‑year linear |
| Community Airdrop | 10% | 100,000,000 | At Token Generation Event |
| Core Contributors | 15% | 150,000,000 | 4‑year linear vesting, 1‑year cliff |
| Seed (Optional) | 5% | 50,000,000 | 2‑year vesting, 6‑month cliff |
| Reserve | 5% | 50,000,000 | DAO‑controlled, for strategic grants and emergencies |

---

## 3. Utility

INTP is the economic and governance layer of the protocol.

- **Governance** — Vote on fee parameters, treasury allocations, contract upgrades, and ecosystem grants.
- **Solver Staking** — Solvers must stake INTP to accept high‑value intents. Staked tokens are slashed if the solver fails to deliver.
- **Premium Access** — Users pay INTP for ad‑free, privacy‑maximal service.
- **Data Marketplace** — Buyers pay INTP to query anonymised intent data. 70% goes to users, 20% to Treasury, 10% to computation providers.
- **Protocol Fee Capture** — Every fulfilled intent pays 0.1% to the Treasury, governed by token holders.

---

## 4. Value Accrual

1. **Protocol Fee (0.1%)** → flows to the Treasury, governed by token holders.
2. **Solver Staking** → locked INTP reduces circulating supply as solver adoption grows.
3. **Premium Subscriptions** → direct token payments for enhanced service.
4. **Data Marketplace** → buyers must hold INTP to query anonymised intent data.

---

## 5. Early Builder Incentives

| Tier | Requirement | INTP Allocation |
|---|---|---|
| **Pioneer** | 100 fulfilled intents | 50,000 INTP |
| **Builder** | 1,000 intents + SDK contribution | 200,000 INTP |
| **Architect** | 10,000 intents + new solver category | 1,000,000 INTP |

Allocations are soul‑bound until mainnet launch, then released linearly over 12 months.

---

## 6. Insurance Pool (Solver Slashing Protection)

A dedicated on‑chain Insurance Pool protects users against solver failures and slashing events. In the event a solver fails to deliver a valid zkTLS proof, its staked INTP is slashed and automatically routed to compensate the affected user, without manual intervention.

| Parameter | Value |
|---|---|
| **Source of Funds** | 0.1% protocol fee (portion allocated by DAO vote), solver bond slashing proceeds, voluntary community donations |
| **Initial Capitalisation** | Seeded with **5% of the Reserve allocation** (2,500,000 INTP) after Token Generation Event |
| **Claim Process** | Automatic – slashed solver bonds are routed to the user who submitted the intent |
| **Governance** | DAO votes on coverage limits, asset composition, and risk parameters. All claims are executed by smart contracts without human approval |

*Reference: Models like Symbiotic’s Slashing Insurance Vaults and Aave’s Umbrella staking system are demonstrating the effectiveness of on‑chain, permissionless insurance pools for protocol risk.*

---

## 7. Governance (INTP DAO)

### Who Are the DAO?
The DAO (Decentralized Autonomous Organization) is the collective of **INTP token holders**. There are no board members, no executives, and no central authority. Any person or entity that holds INTP tokens is a DAO member with voting rights proportional to their holdings.

### How the DAO Works
1. **Proposal Creation** – Any token holder with a minimum threshold of INTP can submit a proposal (e.g., changing a fee, allocating treasury funds, upgrading a contract).
2. **Discussion Period** – The community debates the proposal on forums (Discourse, Discord) for 3‑7 days.
3. **On‑Chain Voting** – Token holders cast votes via Snapshot or similar platforms. Voting power is **1 token = 1 vote**.
4. **Execution** – If a proposal passes (quorum met + majority yes), it enters a **48‑hour timelock** and is then automatically executed by the protocol’s smart contracts.

### Why It Matters
- **No single point of control** – the Treasury cannot be moved without a successful DAO vote.
- **Transparency** – Every proposal, vote, and fund movement is recorded on‑chain.
- **Direct accountability** – token holders collectively decide the protocol’s future, aligning incentives with the community.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

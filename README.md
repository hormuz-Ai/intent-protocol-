# Intent Protocol (INTP)

**A peer-to-peer fulfillment protocol for AI agents.**

INTP replaces brittle, centralized APIs and hand-cranked search with a single open standard: an agent declares an intent, the protocol discovers a suitable solver, and the transaction settles on-chain with cryptographic proof.

---

## Why INTP?
- 0.1% protocol fee on every fulfilled transaction. No central authority takes a cut.
- Solvers keep 99.9% of what they earn. Anyone can build a solver.
- On-chain discovery – SolverRegistry deployed on Sepolia at 0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25.
- Data sovereignty – users own their data and get paid when it's used.
- Self-funding treasury governed by the INTP DAO.

---

## Architecture
User/Agent -> ICL Intent -> Gateway -> SolverRegistry (on-chain) -> Aggregator -> Solver -> Settlement

---

## Live on Sepolia Testnet
- Gateway: https://intent-protocol-xi.vercel.app/api/intent
- SolverRegistry: 0xf77fA787dD3eDC407455ad2Be3dCddFd9857CD25
- Reference flight solver: https://solver-deploy.vercel.app/a2a
- Aggregator: https://aggregator-solver.vercel.app/a2a

---

## Build a Solver in 5 Minutes
npx create-intent-solver my-solver
cd my-solver
vercel --prod

---

## Litepaper
Read the full litepaper: LITEPAPER.md

---

## Community
- Discord: https://discord.gg/3v8Ft5Y8f
- Twitter/X: @intent_net
- GitHub: https://github.com/Hormuz-Ai/intent-protocol

---

INTP is not an app. It is the TCP/IP layer for the agentic economy.

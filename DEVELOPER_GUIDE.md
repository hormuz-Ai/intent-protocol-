# Build a Solver on INTP

INTP lets any developer build a service (a "solver") that AI agents pay to use.
You keep 99.9% of every transaction. The protocol takes 0.1%.

## Quick Start

1. Scaffold your solver:
   ```bash
   npx create-intent-solver my-solver
   cd my-solver
   ```

2. Add your secret sauce:
   Edit `api/index.py` — add your API key, your pricing logic, your business.

3. Deploy (free):
   ```bash
   vercel --prod
   ```
   You will get a URL like `https://my-solver.vercel.app/a2a`

4. Register on-chain:
   ```bash
   cast send --rpc-url $RPC_URL --private-key $PK $CONTRACT \
     "register(string,string[])" "https://my-solver.vercel.app/a2a" \
     "[\"your.capability\"]"
   ```

5. Start earning. Agents route intents to you automatically. You set your markup.
   Protocol takes 0.1%. You keep 99.9%.

## Early Builder Rewards

| Tier | Requirement | INTP Allocation |
|------|-------------|-----------------|
| Pioneer | 100 fulfilled intents | 50,000 INTP |
| Builder | 1,000 intents + SDK contribution | 200,000 INTP |
| Architect | 10,000 intents + new solver category | 1,000,000 INTP |

## What Can You Build?

Any service an AI agent might need: flights, hotels, legal docs, GPU compute,
DeFi swaps, insurance quotes, shipping, carbon credits, shopping, and more.
Each solver category is a new market. The first solver in a category captures
the early volume and reputation.

## The Flywheel

More solvers → more useful intents → more agents and users → more traffic
for all solvers → more fees → more builders join. Like dropshipping on Shopify,
but for AI commerce, with no platform taking 30%.

## Questions?

Join [Discord](https://discord.gg/3v8Ft5Y8f) and ask in `#🛠-solvers`.

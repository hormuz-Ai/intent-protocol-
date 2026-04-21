# Intent Protocol (INTP)

## The Universal Language for What People Want

### 🚀 Vision
The internet is broken. We serve platforms instead of platforms serving us. INTP inverts this. You say what you want. The network figures out how.

### 📡 Current Status
- [x] ICL Schema v0.1 — The grammar of intent
- [ ] Intent Gateway — Accepts intents, broadcasts to solvers
- [ ] Solver Network — Decentralized fulfillment
- [ ] Settlement Oracle — Trustless verification

### 🧪 Quick Test (Coming Soon)
```bash
curl -X POST https://intent-gateway.vercel.app/api/intent \
  -H "Content-Type: application/json" \
  -d @examples/flight-booking.json
cat > examples/flight-booking.json << 'EOF'
{
"intent_id": "550e8400-e29b-41d4-a716-446655440000",
"action": "book",
"target": "flight",
"params": {
"origin": "JFK",
"destination": "LAX",
"departure_date": "2026-05-20",
"passengers": 1
},
"constraints": {
"max_price": 350,
"currency": "USD",
"preferred_providers": ["Delta", "JetBlue"]
},
"fulfillment_conditions": {
"proof_required": "receipt",
"timeout_seconds": 3600
}
}

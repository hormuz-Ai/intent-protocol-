#!/bin/bash
GATEWAY="https://intent-protocol-xi.vercel.app/api/intent"
echo "🚀 INTP Economy Engine Started. Target: \$1,000,000 USD."
i=1
while true; do
  curl -s -X POST "$GATEWAY" -H "Content-Type: application/json" \
    -d '{"action":"book","target":"flight","params":{"origin":"JFK","destination":"LAX","departure_date":"2026-05-10"},"constraints":{"max_price":500}}' > /dev/null
  curl -s -X POST "$GATEWAY" -H "Content-Type: application/json" \
    -d '{"action":"rent","target":"compute","params":{"gpu":"H100","hours":1}}' > /dev/null
  curl -s -X POST "$GATEWAY" -H "Content-Type: application/json" \
    -d '{"action":"book","target":"freight","params":{"origin":"Shanghai","destination":"Rotterdam","containers":1}}' > /dev/null
  
  if (( i % 50 == 0 )); then
    echo "✅ Processed $i intents (Target: 2,857 for \$1M). Keep building."
  fi
  ((i++))
  sleep 2
done

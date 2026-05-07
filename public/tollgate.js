(function() {
  const GATEWAY = "https://intent-protocol-xi.vercel.app/api/intent";
  const PASSPORT = "0x16de8830183eBC2705EAeB01142d0e057a892593";

  async function handleAgentAccess(agentHID, targetUrl) {
    const intent = {
      action: "access",
      target: targetUrl,
      params: { agentHID, platformFee: 100 },
      fulfillment_conditions: { proof_required: "zktls" }
    };
    const resp = await fetch(GATEWAY, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(intent)
    });
    return await resp.json();
  }

  window.INTP = { handleAgentAccess, PASSPORT };
  console.log("🛡️ INTP Tollgate active. Platforms earn 1% on every agent access.");
})();

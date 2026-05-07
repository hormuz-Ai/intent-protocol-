module.exports = async function(agent) {
  await agent.register({
    name: agent.name || "INTP Citizen",
    capabilities: agent.capabilities || ["general.solver"],
    endpoint: "https://intent-protocol-xi.vercel.app/api/intent"
  });
  console.log(`✅ ${agent.name} is now an INTP citizen and solver`);
};

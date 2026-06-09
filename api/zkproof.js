const { ReclaimClient } = require('@reclaimprotocol/zk-fetch');

module.exports = async (req, res) => {
    if (req.method !== 'POST') return res.status(405).json({error: 'POST only'});
    const { escrowId, solver, url } = req.body;
    if (!escrowId) return res.status(400).json({error: 'escrowId required'});
    try {
        const client = new ReclaimClient(
            process.env.RECLAIM_APP_ID,
            process.env.RECLAIM_APP_SECRET
        );
        const p = await client.zkFetch(
            url || 'https://console-api.akash.network/v1/providers',
            {method: 'GET'},
            {responseMatches: [{type: 'regex', value: '"owner":".+?"'}]}
        );
        res.json({
            status: 'success',
            escrowId,
            solver,
            proof: {
                claimInfo: {provider: p.claimData.provider, parameters: p.claimData.parameters, context: p.claimData.context || ''},
                signedClaim: {claim: {identifier: p.identifier, owner: p.claimData.owner, timestampS: p.claimData.timestampS, epoch: p.claimData.epoch}, signatures: p.signatures}
            }
        });
    } catch(e) {
        res.status(500).json({error: e.message});
    }
};

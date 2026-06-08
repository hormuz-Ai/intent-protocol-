const { ReclaimClient } = require("@reclaimprotocol/zk-fetch");
const { ethers } = require("ethers");
const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
const wallet = new ethers.Wallet(process.env.GHOST_PK).connect(provider);
const ESCROW = "0xc9F455fAD53311D35F9965b90Ba6E892E3225f24";
const ADAPTER = "0xB6501a59A3DD0348F3e5f961f17b58e1e5948190";
const TOPIC = "0xe3ad398758b9cbdf4196c5d060a1aebae967b4f9115c7394e937cbb46f449587";
const MY_ADDR = wallet.address.toLowerCase();
const adapterIface = new ethers.Interface([{name:"submitVerifiedWork",type:"function",inputs:[{name:"intentId",type:"bytes32"},{name:"solver",type:"address"},{name:"proof",type:"tuple",components:[{name:"claimInfo",type:"tuple",components:[{name:"provider",type:"string"},{name:"parameters",type:"string"},{name:"context",type:"string"}]},{name:"signedClaim",type:"tuple",components:[{name:"claim",type:"tuple",components:[{name:"identifier",type:"bytes32"},{name:"owner",type:"address"},{name:"timestampS",type:"uint32"},{name:"epoch",type:"uint32"}]},{name:"signatures",type:"bytes[]"}]}]}]}]);
const processed = new Set();

async function handleIntent(escrowId) {
    if (processed.has(escrowId)) return;
    processed.add(escrowId);
    console.log("Intent detected:", escrowId);
    try {
        const client = new ReclaimClient(process.env.RECLAIM_APP_ID, process.env.RECLAIM_APP_SECRET);
        const p = await client.zkFetch("https://console-api.akash.network/v1/providers",{method:"GET"},{responseMatches:[{type:"regex",value:"\"owner\":\".+?\""}]});
        console.log("Proof OK:", p.identifier);
        const proof = {claimInfo:{provider:p.claimData.provider,parameters:p.claimData.parameters,context:p.claimData.context||""}, signedClaim:{claim:{identifier:p.identifier,owner:p.claimData.owner,timestampS:p.claimData.timestampS,epoch:p.claimData.epoch},signatures:p.signatures}};
        const calldata = adapterIface.encodeFunctionData("submitVerifiedWork",[escrowId,wallet.address,proof]);
        const tx = await wallet.sendTransaction({to:ADAPTER,data:calldata,gasLimit:500000,type:0});
        console.log("Submit tx:", tx.hash);
        console.log("https://basescan.org/tx/"+tx.hash);
    } catch(e) { console.error("Error:", e.shortMessage||e.message); }
}

(async () => {
    console.log("INTP Worker listening...");
    console.log("Solver:", wallet.address);
    let lastBlock = await provider.getBlockNumber();
    console.log("From block:", lastBlock);
    while(true) {
        try {
            const current = await provider.getBlockNumber();
            if (current > lastBlock) {
                try {
                    const logs = await provider.getLogs({address:ESCROW,topics:[TOPIC],fromBlock:lastBlock+1,toBlock:current});
                    for (const log of logs) {
                        const escrowId = log.topics[1];
                        const data = log.data.replace("0x","");
                        const solverAddr = "0x" + data.slice(64,128).slice(24);
                        console.log("Deposit found, solver:", solverAddr);
                        if (solverAddr.toLowerCase() === MY_ADDR) await handleIntent(escrowId);
                    }
                } catch(e) {}
                lastBlock = current;
            }
        } catch(e) {}
        await new Promise(r => setTimeout(r, 5000));
    }
})();

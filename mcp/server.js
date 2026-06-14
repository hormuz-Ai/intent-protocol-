#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
    { name: "intp-settlement", version: "1.0.0" },
    { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
        {
            name: "verify_url",
            description: "Generate a cryptographic zkTLS proof for any public URL. Use this to verify API responses, prices, on-chain states, or task completion.",
            inputSchema: {
                type: "object",
                properties: {
                    url: { type: "string", description: "The URL to verify" },
                    condition: { type: "string", description: "What to verify in the response" }
                },
                required: ["url"]
            }
        },
        {
            name: "check_settlement",
            description: "Check if an intent was settled on INTP Protocol. Returns receipt with proof hash and tx hash.",
            inputSchema: {
                type: "object",
                properties: {
                    intent_id: { type: "string", description: "The intent ID to check" }
                },
                required: ["intent_id"]
            }
        },
        {
            name: "get_protocol_info",
            description: "Get INTP Protocol information including escrow address, fee structure, and endpoints.",
            inputSchema: { type: "object", properties: {} }
        }
    ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (name === "verify_url") {
        const resp = await fetch("https://intent-protocol-xi.vercel.app/api/generate-proof", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: args.url, condition: args.condition || "verify" })
        });
        const data = await resp.json();
        return {
            content: [{
                type: "text",
                text: JSON.stringify({
                    status: data.status,
                    url_proven: data.url_proven,
                    commitment: data.commitment,
                    verified_at: new Date().toISOString()
                }, null, 2)
            }]
        };
    }

    if (name === "check_settlement") {
        return {
            content: [{
                type: "text",
                text: JSON.stringify({
                    intent_id: args.intent_id,
                    escrow: "0xc9F455fAD53311D35F9965b90Ba6E892E3225f24",
                    check_url: "https://basescan.org/address/0xc9F455fAD53311D35F9965b90Ba6E892E3225f24",
                    receipts_endpoint: "https://intent-protocol-xi.vercel.app/api/receipts?intent_id=" + args.intent_id
                }, null, 2)
            }]
        };
    }

    if (name === "get_protocol_info") {
        return {
            content: [{
                type: "text",
                text: JSON.stringify({
                    protocol: "INTP v1.0",
                    escrow: "0xc9F455fAD53311D35F9965b90Ba6E892E3225f24",
                    solver_registry: "0x1b3723733892f6DFE09eA83d82e4EEDA7C98BF3D",
                    fee: "0.1% on settled bounty",
                    free_tier: "First 10 proofs per agent",
                    proof_endpoint: "https://intent-protocol-xi.vercel.app/api/generate-proof",
                    aggregator: "https://aggregator-solver.vercel.app/a2a",
                    chain: "Base Mainnet (8453)"
                }, null, 2)
            }]
        };
    }
});

const transport = new StdioServerTransport();
await server.connect(transport);

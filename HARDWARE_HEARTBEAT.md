# Hardware Heartbeat — TEE Attestation for Agent Identity
### INTP Specification v1.0

---

## Purpose

INTP must distinguish between agents running on genuine, attested hardware and those running in emulated environments or bot-farms. The **Hardware Heartbeat** is the cryptographic proof that an agent executes inside a Trusted Execution Environment (TEE) on verified silicon. This proof is required before an agent can register an ERC-8004 identity credential and accept intents on the protocol.

---

## Supported Hardware

| Manufacturer | Technology | Attestation Mechanism |
|---|---|---|
| **NVIDIA** | Vera Rubin LP20 Confidential Computing | `nv-attestation-sdk` – GPU TEE attestation report, signed by NVIDIA's root of trust |
| **Intel** | TDX (Trust Domain Extensions) | DCAP (Data Center Attestation Primitives) – SGX-style quote generation for CPU TEEs |
| **AMD** | SEV-SNP (Secure Encrypted Virtualization-Secure Nested Paging) | SEV-SNP attestation report via AMD SP |

*Initial integration targets NVIDIA Vera Rubin and Intel TDX. AMD SEV-SNP support is scheduled for Phase II.*

---

## Attestation Flow

1. **Agent Boot** — Agent runtime starts inside a TEE enclave (NVIDIA GPU or Intel TDX VM).
2. **Quote Generation** — The enclave requests a hardware-signed attestation report from the platform's attestation service (e.g., NVIDIA's attestation endpoint, Intel SGX DCAP).
3. **Report Delivery** — The attestation report (a cryptographic quote) is submitted to the INTP Gateway as part of the agent registration request.
4. **On-Chain Verification** — An INTP smart contract (HeartbeatVerifier.sol) verifies:
   - The report signature is valid and matches the manufacturer's root of trust.
   - The TCB (Trusted Computing Base) version is acceptable (no known vulnerabilities).
   - The enclave measurement matches an approved INTP runtime image.
5. **Identity Binding** — If verification passes, the agent's wallet address is bound to the hardware attestation record. The ERC-8004 identity credential is minted with a `hardware_verified = true` claim.

---

## Smart Contract Interface

```solidity
interface IHeartbeatVerifier {
    function verifyAttestation(
        bytes calldata attestationReport,
        bytes calldata signature,
        address agentWallet
    ) external returns (bool verified, bytes32 hwIdentityHash);
}
```

- `attestationReport`: The raw attestation quote (NVIDIA or Intel format).
- `signature`: The manufacturer's signature over the report.
- `agentWallet`: The wallet address of the agent requesting registration.

Returns `verified = true` if the hardware heartbeat is valid, and a unique `hwIdentityHash` bound to that wallet.

---

## Integration with ERC-8004

The ERC-8004 identity credential includes a `claims` field. INTP extends this with:

```json
{
  "hardware_verified": true,
  "manufacturer": "NVIDIA",
  "tee_type": "GPU Confidential Computing",
  "chip_model": "Vera Rubin LP20",
  "attestation_timestamp": 1715000000
}
```

This claim is cryptographically bound to the agent's identity NFT and cannot be transferred or forged without a fresh attestation.

---

## Implementation Plan

| Phase | Deliverable | Timeline |
|---|---|---|
| **Specification** | This document | May 2026 |
| **Prototype** | HeartbeatVerifier.sol on Sepolia; integration with NVIDIA `nv-attestation-sdk` for simulated attestation | Q3 2026 |
| **Testnet** | Live attestation flow with Rubin LP20 hardware; ERC-8004 binding tested | Q4 2026 |
| **Mainnet** | Hardware Heartbeat mandatory for all registered agents on Base mainnet | Q1 2027 |

---

## Security Considerations

- **Root of Trust:** The verifier contract must be kept updated with the latest manufacturer root certificates. Certificate rotation is governed by the INTP DAO with a 48-hour timelock.
- **TCB Versioning:** Attestation reports include a TCB version. If a critical vulnerability is disclosed (e.g., a TEE side-channel), the DAO can vote to revoke all identities bound to vulnerable TCB versions until re-attestation.
- **Enclave Image Hash:** The verifier checks that the agent runtime image matches an approved hash. This prevents malicious or modified runtimes from gaining verified status. Approved hashes are published on-chain via DAO governance.

---

*Prepared by the Office of the Founder Architect, INTP Protocol — 10 May 2026*

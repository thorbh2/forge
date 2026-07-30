# Forge

Idea and proposal review with milestones, risks and public sources.

Forge is a review bench for proposals. It keeps idea specs, milestones, risk notes and source material together before GenLayer produces a decision.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://thorbh2-forge.vercel.app |
| GitHub | https://github.com/thorbh2/forge |
| Contract | https://explorer-studio.genlayer.com/address/0xa36eb7430894C299393647Fe21Ed30D7C3dBB75c |

## Chain Record

- Network: GenLayer Studionet
- Chain ID: 61999
- Contract: `0xa36eb7430894C299393647Fe21Ed30D7C3dBB75c`
- Deploy transaction: [0x6aea804a...2a46bb](https://explorer-studio.genlayer.com/tx/0x6aea804ae993f76b39fcee8a4fb85851d2e42b62d6c3779535e1658cb92a46bb)
- Deployed: `2026-06-23T16:54:16.369Z`
- Source: `contracts/forge_v2.py` (41,476 bytes)

## Protocol Path

1. Create an idea.
2. Add specification sources.
3. Register milestones and risks.
4. Run review.
5. Challenge or archive the result.

The frontend reads idea records, risk lists, milestone state and recent review output. Contract state is public; write actions still require a connected wallet on GenLayer Studionet.

## Finalized Smoke

| Action | Transaction |
| --- | --- |
| `set_forge_standard` | [0xb58dbf05...5d955d](https://explorer-studio.genlayer.com/tx/0xb58dbf055b9e0d088a782ae0652e7abfac82c789ef86779a2dd04ba0d55d955d) |
| `create_idea` | [0xee54b1aa...1ad7a2](https://explorer-studio.genlayer.com/tx/0xee54b1aa8c18f3b8fe824509cd21568fb44d1935d83fb83dcd48cf9d101ad7a2) |
| `add_source_node` | [0xbc39991b...45cd8d](https://explorer-studio.genlayer.com/tx/0xbc39991b004ecec774a590eab547bcaf2f5ffc2039380af76d0c470cd045cd8d) |
| `add_source_github` | [0x26b84eb9...b124cf](https://explorer-studio.genlayer.com/tx/0x26b84eb91d4705805cd19f08de6f16eead3db0ffee5631fde5572e8e48b124cf) |
| `add_milestone` | [0x225a6bc2...28562b](https://explorer-studio.genlayer.com/tx/0x225a6bc2ce9a7aaabb972fe77dce8cdfeef0877e603c31db842c4cc22e28562b) |
| `add_risk` | [0x224efe1f...1e968b](https://explorer-studio.genlayer.com/tx/0x224efe1f6ee2ab4e134edc25828c4cece3780c180e4b2f9c86d574dede1e968b) |

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.

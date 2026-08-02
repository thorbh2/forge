# Forge

Idea and proposal review with milestones, risks and public sources.

Forge is a review bench for proposals. It keeps idea specs, milestones, risk notes and source material together before GenLayer produces a decision.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://forge-proposal-review.vercel.app |
| GitHub | https://github.com/thorbh2/forge |
| Contract | https://explorer-studio.genlayer.com/address/0xd5cb7A1C7B17395AF5dC3B0d68e8b7998D454EfD |

## Chain Record

- Network: GenLayer Studionet
- Chain ID: 61999
- Contract: `0xd5cb7A1C7B17395AF5dC3B0d68e8b7998D454EfD`
- Deploy transaction: [0xf7b835ff...cffc4b](https://explorer-studio.genlayer.com/tx/0xf7b835ff1e277c9c8bddbabbfd80a7ea8b1309c2a6d8e61796a26cec0ecffc4b)
- Deployed: `2026-08-02T20:55:44.732Z`
- Source: `contracts/forge_v2.py` (48,689 bytes)
- Source SHA-256: `36709bf42a8cbe8f0280717f7444a297b9d1fde73051a52082d7523b1d16ba91`

## Protocol Path

1. Create a proposal with category and operating context.
2. Add independent sources, milestones with acceptance criteria, and material risks.
3. Run exact-field validator review across every settlement-changing result.
4. File challenge or appeal evidence under explicit deadlines.
5. Use permissionless expiry when an adverse filing is left unresolved.

The frontend reads idea records, risk lists, milestone state and recent review output. Contract state is public; write actions still require a connected wallet on GenLayer Studionet.

## Verification

`tests/test_forge.py` exercises the complete source, milestone and risk workflow, exact validator agreement, and both permissionless filing-expiry fallbacks. The direct GenVM suite passes 3/3.

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.

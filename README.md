# Forge V2

A GenLayer build-pipeline reviewer.

The project is packaged as a real protocol surface, not a placeholder page: the contract stores records, exposes read models and records smoke-tested writes.

## Forge Brief

- Project folder: `projects/27-forge`
- Frontend: static browser app
- Contract package: `contracts/` plus `deployment.json`
- Build status: Schema-valid (41476 bytes, 17 write + 22 view); deployed + 16 write smoke txs finalized incl 3 GenLayer reasoning calls; 40/40 read tests passed; legacy frontend shape verified; app.js repointed.
- QA notes: Upgraded from a 5.6KB pitch/review MVP to Forge V2. Smoke: set_forge_standard / create_idea / two add_spec_source calls / add_milestone / add_risk / open_review / review_idea_with_genlayer / open_challenge_window / submit_challenge / resolve_challenge_with_...

## Contract Receipt

- Network: studionet (61999)
- Contract: [0xa36eb7430894C299393647Fe21Ed30D7C3dBB75c](https://explorer-studio.genlayer.com/contracts/0xa36eb7430894C299393647Fe21Ed30D7C3dBB75c)
- Deploy tx: [0x6aea804a...2a46bb](https://explorer-studio.genlayer.com/tx/0x6aea804ae993f76b39fcee8a4fb85851d2e42b62d6c3779535e1658cb92a46bb)
- Deployed at: 2026-06-23T16:54:16.369Z
- Smoke writes recorded: 16

## Protocol Mechanics

- Primary source: `contracts/forge_v2.py` (41,476 bytes)
- Public write/action methods: 17
- Read methods: 22
- GenLayer features: live web rendering, LLM adjudication, validator-comparative consensus, indexed storage, append-only collections

Typical flow: `create_idea` -> `open_review` -> `submit_challenge` -> `review_idea_with_genlayer` -> `resolve_challenge_with_genlayer` -> `open_challenge_window` -> `submit_appeal` -> `archive_idea`

Useful reads: `get_idea_count`, `get_stats`, `get_idea`, `get_idea_record`, `get_recent_ideas`, `get_ideas_by_status`, `get_ideas_by_category`, `get_author_ideas`

The contract is deliberately larger than a one-method demo. It keeps lifecycle state, evidence records and read endpoints so the UI can show real project state instead of static copy.

## Inspect The App

```powershell
cd <private-workspace-root>
npm run preview:start
npm run preview:project -- 27-forge
```

Open http://localhost:8080/27-forge/.

## Smoke Transactions

- set_forge_standard: [0xb58dbf05...5d955d](https://explorer-studio.genlayer.com/tx/0xb58dbf055b9e0d088a782ae0652e7abfac82c789ef86779a2dd04ba0d55d955d)
- create_idea: [0xee54b1aa...1ad7a2](https://explorer-studio.genlayer.com/tx/0xee54b1aa8c18f3b8fe824509cd21568fb44d1935d83fb83dcd48cf9d101ad7a2)
- add_source_node: [0xbc39991b...45cd8d](https://explorer-studio.genlayer.com/tx/0xbc39991b004ecec774a590eab547bcaf2f5ffc2039380af76d0c470cd045cd8d)
- add_source_github: [0x26b84eb9...b124cf](https://explorer-studio.genlayer.com/tx/0x26b84eb91d4705805cd19f08de6f16eead3db0ffee5631fde5572e8e48b124cf)
- add_milestone: [0x225a6bc2...28562b](https://explorer-studio.genlayer.com/tx/0x225a6bc2ce9a7aaabb972fe77dce8cdfeef0877e603c31db842c4cc22e28562b)
- add_risk: [0x224efe1f...1e968b](https://explorer-studio.genlayer.com/tx/0x224efe1f6ee2ab4e134edc25828c4cece3780c180e4b2f9c86d574dede1e968b)
- open_review: [0x8df8123e...85be31](https://explorer-studio.genlayer.com/tx/0x8df8123e3624c39c43eaf7cc72c7962dcfe6677a7e3915b7534c2673dc85be31)
- review: [0xea727ef5...21cf25](https://explorer-studio.genlayer.com/tx/0xea727ef5dc9a76f80a5e614e4b4d805be7819c7d3f98661b23968434f621cf25)

## Shipping Notes

```powershell
cd <private-workspace-root>
npm run publish:project -- -Project 27-forge -Repo https://github.com/aspro45/<repo-name>.git
```

Replace `<repo-name>` with the GitHub repository name before publishing.

## Security Notes

- Private keys and local vault files are not part of this repository.
- Public addresses, contract source, deployment metadata and frontend code are safe to publish.
- Vercel should receive only this project folder, never the workspace dashboard or vault data.

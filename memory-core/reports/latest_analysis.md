# REQUIEM MEMORY CORE ANALYSIS REPORT

Analysis: ANL-001
Generated: 2026-09-24T18:59:13
Status: COMPLETED_WITH_WARNINGS
Project: REQUIEM (requiem-tauri)

> Findings are rule matches, not evaluations. Analysis does not approve or reject changes.

## Source

Change record: CHG-001 (status at analysis: APPROVED)

record_sha256: e2cf2ed838ad662080e04ed36134e91d55128fd1a55372e722f392581f30c8f6

facts_sha256: 4abd791e6bf96515451debe2e5b11728d89b3556c5e9d186262a83bbce883c61

Comparison: CMP-001-003

| | Snapshot | source_sha256 |
|---|---|---|
| From | SNAP-001 | 356e7a7adb667b07784e78231e3df5d84b79f1841dabd2a8a24a3fe378c0b91f |
| To | SNAP-003 | f589ec27fa3c1b998f1f5d48440e33dc27903fe23203f11be8d1758327217913 |

## Rules and map

Rules: revision 1, sha256 ea79b65a8c176771a8f8cfb98779d5ef75244985fdee3c9b519ca51981ed9efc

Architecture map: revision 2, status DRAFT, sha256 32a817ca3c2a0c90ff0df6fefb191473e641f98bd68550beda51622fd03bafc0

## Summary

| Class | Files |
|---|---|
| Added | 0 |
| Removed | 0 |
| Modified | 1 |
| Unverified | 0 |
| Unchanged | 61 |

Findings: attention 0 | notice 1 | info 0

Size delta (bytes): added 0, removed 0, modified 3, total 3; unverified excluded: 0

## Findings

### Notice

- ANL-001/F-1 [S-UNMAPPED] Paths are not covered by the architecture map.
  - CHG-001/1 `src/App.jsx`
  - evidence: paths: `src/App.jsx`

## Entries

| Entry | Class | Path | Category | Zone |
|---|---|---|---|---|
| CHG-001/1 | modified | `src/App.jsx` | source | unmapped |

## Zones

| Zone | Added | Removed | Modified | Unverified |
|---|---|---|---|---|
| unmapped | 0 | 0 | 1 | 0 |

## Categories

| Category | Added | Removed | Modified | Unverified |
|---|---|---|---|---|
| source | 0 | 0 | 1 | 0 |

## Coverage

Files in SNAP-003: 62

| Zone | Files |
|---|---|
| unmapped | 62 |

| Category | Files |
|---|---|
| manifest | 2 |
| lockfile | 2 |
| vcs | 2 |
| tool-config | 4 |
| source | 22 |
| style | 2 |
| markup | 1 |
| data | 5 |
| documentation | 1 |
| image | 19 |
| archive | 2 |
| uncategorized | 0 |

### Unmapped paths (62)

- `.gitignore`
- `README.md`
- `index.html`
- `package-lock.json`
- `package.json`
- `postcss.config.js`
- `public/tauri.svg`
- `public/vite.svg`
- `src-tauri/.gitignore`
- `src-tauri/Cargo.lock`
- `src-tauri/Cargo.toml`
- `src-tauri/build.rs`
- `src-tauri/capabilities/default.json`
- `src-tauri/gen/schemas/acl-manifests.json`
- `src-tauri/gen/schemas/capabilities.json`
- `src-tauri/gen/schemas/desktop-schema.json`
- `src-tauri/gen/schemas/windows-schema.json`
- `src-tauri/icons/128x128.png`
- `src-tauri/icons/128x128@2x.png`
- `src-tauri/icons/32x32.png`
- `src-tauri/icons/Square107x107Logo.png`
- `src-tauri/icons/Square142x142Logo.png`
- `src-tauri/icons/Square150x150Logo.png`
- `src-tauri/icons/Square284x284Logo.png`
- `src-tauri/icons/Square30x30Logo.png`
- `src-tauri/icons/Square310x310Logo.png`
- `src-tauri/icons/Square44x44Logo.png`
- `src-tauri/icons/Square71x71Logo.png`
- `src-tauri/icons/Square89x89Logo.png`
- `src-tauri/icons/StoreLogo.png`
- `src-tauri/icons/icon.icns`
- `src-tauri/icons/icon.ico`
- `src-tauri/icons/icon.png`
- `src-tauri/src/lib.rs`
- `src-tauri/src/main.rs`
- `src-tauri/tauri.conf.json`
- `src.zip`
- `src/App.css`
- `src/App.jsx`
- `src/app/AppRoot.jsx`
- `src/app/layout/MainLayout.jsx`
- `src/app/layout/index.js`
- `src/app/shell/RequiemShell.jsx`
- `src/app/shell/WindowFrame.jsx`
- `src/app/shell/index.js`
- `src/app/workspace/Workspace.jsx`
- `src/assets/react.svg`
- `src/core.zip`
- `src/core/configuration/index.js`
- `src/core/contracts/EngineCommand.js`
- `src/core/contracts/EngineResponse.js`
- `src/core/contracts/EnvironmentState.js`
- `src/core/contracts/OperationRequest.js`
- `src/core/contracts/OperationResult.js`
- `src/core/contracts/UserIntent.js`
- `src/core/environment/index.js`
- `src/core/intelligence/index.js`
- `src/core/operations/index.js`
- `src/index.css`
- `src/main.jsx`
- `tailwind.config.js`
- `vite.config.js`

### Uncategorized paths (0)

- none

## Warnings

- Architecture map is DRAFT (not approved).

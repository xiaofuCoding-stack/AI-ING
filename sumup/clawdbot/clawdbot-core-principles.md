# clawdbot - Core Technical Principles

## Overview

**Project type**: Node.js application (TypeScript, ESM).  
**Runtime**: Node ≥22.  
**Representative stack**: @agentclientprotocol/sdk, @mariozechner/pi-agent-core, Baileys/grammy/Bolt/discord.js for channels, TypeBox, express/ws, Lit for Control UI.

## Core Design Principles

1. **Local-first Gateway** — One control plane you run; all channels and clients connect to it. No mandatory cloud backend for core operation.
2. **Channel-agnostic session model** — Sessions and routing are defined in terms of agent, thread, and identity; channels are adapters.
3. **Single-binary / single-image UX** — One `clawdbot` CLI and one Gateway process (or container) for normal setups; optional daemon install.
4. **Security by default** — DM pairing, allowlists, sandbox for non-main sessions; token/password auth for Control UI and remote access.
5. **Tool safety** — Allow/deny lists, optional Docker sandbox per agent/session; host tools (browser, canvas, nodes) explicitly separated from sandboxed tools.

## Key Abstractions

- **Session** — Logical conversation scope (e.g. main DM, a group); has model, thinking level, tools, routing rules.
- **Channel** — Adapter from an external messaging surface into Gateway’s internal message/session model.
- **Agent** — Configurable identity + model + tools + routing; defaults live under `agents.defaults`, overridable per `agents.list[]`.
- **Node** — Device or companion (macOS/iOS/Android) that can run actions via `node.invoke` (camera, screen, canvas, etc.).
- **Gateway protocol** — WebSocket methods and events for config, sessions, presence, cron, chat runs, etc.

## Architectural Patterns

- **Gateway as hub** — All clients and channels talk to the Gateway; no direct channel–agent linkage.
- **Plugin/skill extensions** — Extensions under `extensions/`, skills under `~/clawd/skills/<name>/SKILL.md`, and plugin-sdk for custom logic.
- **Sandboxing** — Non-main sessions can run tools inside Docker containers (image, scope, prune, allow/deny tools) without putting the Gateway itself in Docker.
- **Remote exposure** — Gateway binds to loopback by default; Tailscale Serve/Funnel or SSH tunnels expose it; auth via token or password.

## Latest Technical Updates

- See **CHANGELOG.md** in the repo and [Releases](https://github.com/clawdbot/clawdbot/releases) for version history.
- **Stable**: tagged `vYYYY.M.D`; **beta**: `vYYYY.M.D-beta.N`; **dev**: `main` branch, dist-tag `dev` when published.
- **Node**: Requires Node ≥22; **pnpm** is the default package manager for from-source builds.
- **Docker**: Official path is `docker-setup.sh` + docker-compose; optional sandbox image (`Dockerfile.sandbox`) for agent isolation.

---
*Content derived from README, gateway/docs, and config schema.*

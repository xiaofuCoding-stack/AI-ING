# clawdbot - Implementation Details

## Technology Stack

| Layer | Tech |
|-------|------|
| Runtime | **Node.js ≥22** |
| Language | **TypeScript** (strict, ESM) |
| Package manager | **pnpm** (workspace), npm/bun supported |
| Build | **tsc** (TypeScript), Vite (UI), scripts for A2UI/canvas |
| UI | **Lit**, Vite, base path via `CLAWDBOT_CONTROL_UI_BASE_PATH` |
| Agent | **@mariozechner/pi-agent-core**, **@agentclientprotocol/sdk** |
| Channels | **@whiskeysockets/baileys**, **grammy**, **@slack/bolt**, **discord.js**, etc. |
| HTTP/WS | **express**, **ws**, **hono** (some surfaces) |
| Config/Validation | **TypeBox**, **json5**, **zod** |
| Logging | **tslog** |

## Key Dependencies

- **@agentclientprotocol/sdk** — Agent Client Protocol
- **@aws-sdk/client-bedrock** — AWS Bedrock models
- **@buape/carbon** — Carbon-style UI
- **@clack/prompts** — CLI prompts
- **@grammyjs/runner**, **@grammyjs/transformer-throttler** — Telegram
- **@homebridge/ciao** — mDNS/Bonjour
- **@line/bot-sdk** — LINE
- **@lydell/node-pty** — PTY for shells
- **@mariozechner/pi-agent-core** — Agent runtime
- **@sinclair/typebox** — JSON Schema / validation
- **@slack/bolt**, **@slack/web-api** — Slack
- **@whiskeysockets/baileys** — WhatsApp
- **chromium-bidi**, **playwright-core** — Browser automation
- **express**, **ws**, **hono** — HTTP/WebSocket
- **sharp** — Image handling
- **sqlite-vec** — Vector storage (e.g. memory)
- **vitest** — Tests

## Implementation Patterns

- **ESM only** (`"type": "module"`), path imports with `.js` extension.
- **Single Gateway process**: one Node process runs Gateway + in-process agent by default; no separate agent process required.
- **Config**: TypeBox schema + JSON5 file (`~/.clawdbot/clawdbot.json`), env overrides via `CLAWDBOT_*`.
- **CLI**: `src/entry.ts` → respawn/env → Commander; subcommands under `src/commands/`, `src/cli/`.
- **Daemon**: launchd (macOS) / systemd user (Linux) via `onboard --install-daemon`; entrypoint `dist/entry.js gateway`.

## Build and Deployment

- **Build**: `pnpm build` → `tsc` + canvas/A2UI bundle + copy scripts → `dist/`.
- **UI**: `pnpm ui:build` → Vite build of `ui/` → assets copied into Gateway serve path.
- **Package**: `dist/` + docs + extensions + skills; `bin.clawdbot` → `dist/entry.js`.
- **Docker**: `Dockerfile` based on `node:22-bookworm`; install deps → build → `node dist/index.js` (or `gateway` in compose).
- **Cloud**: `fly.toml` (Fly.io), `render.yaml` (Render); both use same Dockerfile, env and mounts differ.

## Configuration

- **File**: `~/.clawdbot/clawdbot.json` (overridable by `CLAWDBOT_CONFIG_PATH`).
- **Schema**: Full reference at [docs.clawd.bot/gateway/configuration](https://docs.clawd.bot/gateway/configuration).
- **High-level keys**: `agent`, `agents`, `channels.*`, `gateway.*`, `tools.*`, `agents.defaults.sandbox`, etc.
- **Secrets**: Token/password in config or env (`CLAWDBOT_GATEWAY_TOKEN`, etc.); channel tokens via env or `channels.<name>.*`.

---
*Content derived from package.json, Dockerfile, docker-compose, and docs.*

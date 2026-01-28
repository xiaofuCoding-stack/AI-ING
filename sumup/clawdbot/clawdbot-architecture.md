# clawdbot - Architecture Overview

## System Architecture

Clawdbot is a **local-first personal AI assistant** built around a central **Gateway** (WebSocket control plane). All channels (WhatsApp, Telegram, Slack, Discord, WebChat, etc.) and clients (CLI, Control UI, macOS/iOS/Android apps) connect to this single Gateway. The Gateway holds sessions, config, cron, presence, and routes messages to the Pi Agent (RPC) for reasoning and tool execution.

```
  Channels (WhatsApp/Telegram/…) + WebChat
               │
               ▼
  ┌─────────────────────────────────────┐
  │            Gateway                  │
  │   (WebSocket + HTTP, default :18789)│
  └──────────────┬──────────────────────┘
                 │
   ┌─────────────┼─────────────┐
   ▼             ▼             ▼
 Pi Agent    CLI / TUI    macOS/iOS/Android
 (RPC)       (control)    (nodes, voice, canvas)
```

## Component Overview

| Component | Role |
|-----------|------|
| **Gateway** | WebSocket server, HTTP (Control UI, WebChat, /health), session/store, config, cron, channel routing |
| **Pi Agent** | RPC-based agent loop (pi-agent-core + ACP), tools (bash, browser, canvas, nodes, cron, sessions, etc.) |
| **Channels** | Adapters per platform (Baileys/WhatsApp, grammY/Telegram, Bolt/Slack, discord.js, etc.) |
| **Control UI** | Lit + Vite SPA, talks to Gateway over WebSocket; settings, sessions, logs, cron, skills |
| **CLI** | Commander-based; `gateway`, `agent`, `message`, `onboard`, `doctor`, `channels`, etc. |
| **Nodes** | Device-side runners (macOS/iOS/Android) for camera, screen, canvas, voice, `node.invoke` |

## Data Flow

1. **Inbound**: User message on a channel → Channel adapter → Gateway routing → Session (main or group) → Agent run (RPC).
2. **Agent**: Receives session context and tools; calls LLM; executes tools (bash, browser, etc.); streams back text/blocks.
3. **Outbound**: Agent output → Gateway → Channel adapter → user-facing reply (plus typing indicators, presence).
4. **Control**: CLI/UI connect via WebSocket; call methods (e.g. `sessions.patch`, `config.get`); receive presence/logs/events.

## Extension Points

- **Channels**: New adapters under `src/channels/` (or extensions) implementing the channel contract (connect, send, receive, typing, etc.).
- **Tools**: Registered in the agent tool registry; can be host-local or sandboxed (Docker) per config.
- **Skills**: `~/clawd/skills/<name>/SKILL.md` and config; wizard and Control UI can install/manage them.
- **Plugins**: `plugin-sdk` and `extensions/` for custom behaviors and integrations.

## Communication Patterns

- **Gateway ↔ clients**: WebSocket JSON-RPC-style methods and events (e.g. `sessions.list`, `presence.subscribe`, `chat.run`).
- **Gateway ↔ Pi Agent**: RPC (in-process or out-of-process) for agent loop and tool dispatch.
- **Gateway ↔ channels**: Platform-specific SDKs (Bolt, grammY, Baileys, etc.); Gateway normalizes to internal message/session model.
- **Remote access**: Tailscale Serve/Funnel or SSH tunnels; Gateway stays bound to loopback, reverse proxy handles HTTPS.

---
*Content derived from project README, docs, and codebase structure.*

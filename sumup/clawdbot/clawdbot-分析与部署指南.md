# Clawdbot 项目分析与部署指南

## 一、项目概述

**Clawdbot** 是一个「可自托管」的个人 AI 助手平台，由 [Clawd](https://clawd.me) 团队维护，核心是你在自己的设备上运行的 **Gateway（控制面）**，通过多种渠道（WhatsApp、Telegram、Slack、Discord、WebChat 等）与你对话，并支持语音、画布、技能等能力。

### 1.1 核心定位

- **本地优先**：Gateway 跑在你自己的机器或服务器上，数据与对话由你控制。
- **多渠道收件箱**：同一套助手，可在 WhatsApp / Telegram / Slack / Discord / Google Chat / Signal / iMessage / WebChat 等渠道统一响应。
- **可扩展**：支持 Skills、插件、多 Agent 路由、Cron、Webhook 等。

### 1.2 技术栈概览

| 类别       | 技术 |
|------------|------|
| 运行时     | **Node.js ≥22**（推荐 22.12+） |
| 包管理     | pnpm（推荐）、npm、bun |
| 语言       | TypeScript（主仓）、Swift（macOS/iOS）、Kotlin（Android） |
| 前端       | Lit、Vite（Control UI） |
| Agent 内核 | @mariozechner/pi-agent-core、ACP（Agent Client Protocol） |
| 渠道适配   | Baileys(WhatsApp)、grammY(Telegram)、Bolt(Slack)、discord.js 等 |

### 1.3 项目结构（简要）

```
project/clawdbot/
├── src/              # 主逻辑（Gateway、CLI、Channels、Agents、Tools…）
├── ui/                # Control UI（Vite + Lit）
├── extensions/        # 渠道/能力扩展
├── apps/              # macOS / iOS / Android 客户端
├── docs/              # 文档（Mintlify）
├── scripts/           # 构建、Docker、E2E 等
├── Dockerfile         # 网关镜像
├── docker-compose.yml
├── fly.toml           # Fly.io 部署
└── render.yaml        # Render 部署
```

---

## 二、系统架构简图

```
  WhatsApp / Telegram / Slack / Discord / … / WebChat
                        │
                        ▼
  ┌─────────────────────────────────────────────────┐
  │                  Gateway                         │
  │            (WebSocket 控制面)                     │
  │             默认 ws://127.0.0.1:18789            │
  └─────────────────────┬───────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   Pi Agent (RPC)    CLI / WebChat   macOS/iOS/Android
   (对话与工具)      (控制与对话)      (节点/语音/画布)
```

- **Gateway**：提供 WebSocket API、HTTP（Control UI、WebChat、健康检查）、会话与通道路由、Cron、配置等。
- **CLI**：`clawdbot` 命令（gateway / agent / message / onboard / doctor 等）通过 entry.js 派发到对应子命令。
- **渠道**：各 channel 连接后，把消息转成统一会话模型，交给 Agent 处理，再回写到对应渠道。

---

## 三、部署方式总览

| 方式           | 适用场景                     | 本节位置   |
|----------------|------------------------------|------------|
| npm 全局安装   | 本机快速体验、开发/调试      | 3.1        |
| 从源码运行     | 二次开发、改代码后本地跑      | 3.2        |
| Docker Compose | 本机/服务器隔离运行、VPS     | 3.3        |
| Fly.io         | 云上常驻、公网 HTTPS         | 3.4        |
| Render         | 云上 Web 服务、托管 Docker   | 3.5        |

---

## 四、部署步骤详解

### 4.1 使用 npm 全局安装（推荐入门）

**环境**：Node ≥22。

```bash
# 安装
npm install -g clawdbot@latest
# 或
pnpm add -g clawdbot@latest

# 一键向导（配置网关、工作区、渠道、技能，并可安装守护进程）
clawdbot onboard --install-daemon
```

向导会引导你完成：

- Gateway 绑定地址、认证方式（token/密码）
- 工作区目录（默认 `~/clawd`）
- 要启用的渠道（WhatsApp / Telegram 等）
- 是否安装系统服务（launchd/systemd），让 Gateway 常驻

之后可：

```bash
# 若未装守护进程，可前台启动网关
clawdbot gateway --port 18789 --verbose

# 发一条消息测试
clawdbot message send --to +1234567890 --message "Hello from Clawdbot"

# 与助手对话（可指定回复渠道）
clawdbot agent --message "Ship checklist" --thinking high
```

升级与自检：

```bash
clawdbot doctor   # 检查配置、DM 策略等
clawdbot update   # 升级（可跟 --channel stable|beta|dev）
```

---

### 4.2 从源码构建与运行（开发/自改代码）

**环境**：Node ≥22，推荐 pnpm。

```bash
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot

pnpm install
pnpm ui:build   # 首次会装 UI 依赖并构建
pnpm build      # 产出 dist/

# 使用本地构建的 CLI 跑向导（可选：安装 daemon）
pnpm clawdbot onboard --install-daemon
```

- `pnpm clawdbot ...`：用 `tsx` 直接跑 TS，不依赖 `dist/`。
- `pnpm build`：生成 `dist/`，可用 `node dist/entry.js ...` 或打包后的 `clawdbot`。

开发时边改边跑网关：

```bash
pnpm gateway:watch   # 监听 TS 变更并重启 gateway
```

---

### 4.3 使用 Docker Compose 部署（本机或 VPS）

**前提**：已安装 Docker 与 Docker Compose v2。

**一键脚本（推荐）**：

在仓库根目录执行：

```bash
cd project/clawdbot
./docker-setup.sh
```

脚本会：

1. 构建镜像 `clawdbot:local`（或 `$CLAWDBOT_IMAGE`）
2. 生成网关 token 并写入 `.env`
3. 以交互方式跑 `clawdbot onboard --no-install-daemon`
4. 启动 `clawdbot-gateway` 容器

常用环境变量（在运行 `docker-setup.sh` 前设置）：

| 变量 | 说明 | 默认 |
|------|------|------|
| `CLAWDBOT_CONFIG_DIR` | 宿主机配置目录 | `$HOME/.clawdbot` |
| `CLAWDBOT_WORKSPACE_DIR` | 工作区目录 | `$HOME/clawd` |
| `CLAWDBOT_GATEWAY_PORT` | 映射到主机的端口 | `18789` |
| `CLAWDBOT_GATEWAY_TOKEN` | 不设则脚本内用 openssl 生成 | - |
| `CLAWDBOT_IMAGE` | 镜像名 | `clawdbot:local` |

手动分步示例：

```bash
docker build -t clawdbot:local -f Dockerfile .
docker compose run --rm clawdbot-cli onboard
docker compose up -d clawdbot-gateway
```

宿主机访问：浏览器打开 `http://127.0.0.1:18789/`，在 Control UI 的「Settings → token」中粘贴脚本输出的 token。

**渠道在容器内配置**（示例）：

```bash
# WhatsApp 扫码登录
docker compose run --rm clawdbot-cli channels login

# Telegram / Discord 等用 token
docker compose run --rm clawdbot-cli channels add --channel telegram --token "<token>"
```

健康检查：

```bash
docker compose exec clawdbot-gateway node dist/index.js health --token "$CLAWDBOT_GATEWAY_TOKEN"
```

如需在 Docker 里用「Agent 沙箱」（非 main 会话跑在容器里），见官方文档 [Sandboxing](https://docs.clawd.bot/gateway/sandboxing) 和仓库内 `docs/install/docker.md`。

---

### 4.4 使用 Fly.io 部署（云端常驻）

**前提**：已安装 [flyctl](https://fly.io/docs/hands-on/install-flyctl/)，并完成 `fly auth login`。

1. **使用仓库内配置**  
   项目根目录已有 `fly.toml`，面向 `gateway` 进程，默认区为 `iad`，可按需改 `primary_region` 和 `app`。

2. **挂载持久化卷**（必须，否则重启数据丢）：

   ```bash
   fly volumes create clawdbot_data --region iad --size 1
   ```

3. **设置密钥**（在 Fly  dashboard 或用 `fly secrets`）：

   - `CLAWDBOT_GATEWAY_TOKEN`（或你采用的认证方式）
   - 若用 Claude/OpenAI 等，按文档配置对应环境变量（如 `CLAUDE_AI_SESSION_KEY` 等，不要写进文档的示例里，仅提醒要设）

4. **部署**：

   ```bash
   fly deploy
   ```

`fly.toml` 里已配置：

- 进程：`node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan`
- 内部 3000，对外 HTTPS，长期运行（`min_machines_running = 1`）
- 挂载点：`/data` → volume `clawdbot_data`

部署完成后用 `fly open` 或给出的 URL 访问；若用 Control UI，需在配置里把「Gateway URL」指到该 HTTPS 地址，并配置好 token。

---

### 4.5 使用 Render 部署（托管 Docker）

**前提**：有 Render 账号，且项目已连到 GitHub 等仓库。

仓库根目录的 `render.yaml` 已定义 Web 服务，要点：

- `runtime: docker`，用项目里的 `Dockerfile` 构建。
- 需要 **持久化盘**：`/data`，用于 state / workspace。
- 环境变量示例（在 Render 面板中配置）：
  - `PORT=8080`（由 Render 注入的端口）
  - `CLAWDBOT_STATE_DIR=/data/.clawdbot`
  - `CLAWDBOT_WORKSPACE_DIR=/data/workspace`
  - `CLAWDBOT_GATEWAY_TOKEN`：可在 Render 里选择 “Generate” 生成随机值

启动命令需与 `Dockerfile` 的 `CMD` 以及你在 Render 里填的「Start Command」一致：通常为 `node dist/index.js gateway --port $PORT --bind lan`（具体以你当前 `Dockerfile`/README 为准）。

若 Render 的 Docker 模式默认不会把 `PORT` 传给 `gateway`，需要在 Start Command 里显式用 `$PORT`。

---

## 五、配置与入口

### 5.1 配置文件位置

- 默认：`~/.clawdbot/clawdbot.json`
- 可通过环境变量 `CLAWDBOT_CONFIG_PATH` 覆盖

### 5.2 最简配置示例

```json5
{
  agent: {
    model: "anthropic/claude-opus-4-5"
  }
}
```

更多选项见：[Configuration](https://docs.clawd.bot/gateway/configuration)

### 5.3 常用环境变量（部署相关）

| 变量 | 含义 |
|------|------|
| `CLAWDBOT_CONFIG_PATH` | 配置文件路径 |
| `CLAWDBOT_STATE_DIR` | 状态与数据目录 |
| `CLAWDBOT_GATEWAY_PORT` | 网关端口 |
| `CLAWDBOT_GATEWAY_TOKEN` | 网关 token 认证 |
| `CLAWDBOT_GATEWAY_BIND` | 绑定地址，如 `loopback` / `lan` |
| `CLAWDBOT_SKIP_CHANNELS` | 开发时跳过渠道，如 `1` |
| `NODE_ENV` | `production` 时关闭部分调试行为 |

---

## 六、入口与命令

- **二进制入口**：`dist/entry.js`（由 `package.json` 的 `bin["clawdbot"]` 指向）。
- **逻辑入口**：`src/entry.ts` 做参数规范化、Node 选项与 respawn，再交给 Commander 子命令。
- **网关子命令**：`gateway`（`gateway run` 等），实际启动的是 `node dist/index.js gateway …`。

常用命令汇总：

```bash
clawdbot onboard [--install-daemon]   # 向导
clawdbot gateway [--port 18789]       # 前台跑网关
clawdbot doctor                      # 检查与修复
clawdbot agent --message "..."       # 与助手对话
clawdbot message send --to <id> --message "..."  # 发消息到指定渠道
clawdbot channels login              # 渠道登录（如 WhatsApp QR）
clawdbot dashboard [--no-open]       # 打开/输出 Control UI 地址
clawdbot doctor --generate-gateway-token   # 生成并写入 token
```

---

## 七、延伸阅读与链接

- 官网与文档：[clawdbot.com](https://clawdbot.com)、[docs.clawd.bot](https://docs.clawd.bot)
- 快速开始：[Getting started](https://docs.clawd.bot/start/getting-started)
- 配置大全：[Gateway configuration](https://docs.clawd.bot/gateway/configuration)
- Docker 详细说明：仓库内 `docs/install/docker.md`
- 安全与加固：[Security](https://docs.clawd.bot/gateway/security)
- 远程访问（Tailscale/SSH）：[Remote](https://docs.clawd.bot/gateway/remote)

---

## 八、本仓库内相关文件索引

- 已有总结（偏骨架，可作补充）：
  - `sumup/clawdbot-architecture.md`
  - `sumup/clawdbot-implementation.md`
  - `sumup/clawdbot-core-principles.md`
- 项目本体与部署相关：
  - `project/clawdbot/README.md`
  - `project/clawdbot/package.json`
  - `project/clawdbot/Dockerfile`、`docker-compose.yml`、`docker-setup.sh`
  - `project/clawdbot/fly.toml`、`project/clawdbot/render.yaml`
  - `project/clawdbot/docs/install/docker.md`

以上为 Clawdbot 的分析摘要与部署路径；按你当前环境（本机 / VPS / Fly / Render）选对应小节逐步执行即可完成部署。

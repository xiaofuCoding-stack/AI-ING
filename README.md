# AI-ING · 一个项目，走在 AI 最前沿

> **专治 FOMO。** 只跟进这一个仓库，你就不会掉队。

AI 变化太快：新模型、新框架、新项目每天刷屏，总怕漏掉什么。**AI-ING** 把「前沿技术」和「最好用的实践」收拢到一处：**精选项目深度拆解 + 可直接复用的 Cursor Skills**，持续更新。你只需要 Watch 这一个 Repo。

---

## ✨ 你会在这里得到什么

| 内容 | 说明 |
|------|------|
| **🔥 最火项目的输出** | 对热门开源项目做**原理 + 架构 + 部署**的整理，放在 `sumup/`，读完就能懂、能上手 |
| **🛠 最好用的 Skills** | 在 Cursor 里即插即用的技能（技术分析、提示词查找、Code Review 等），拿来就能提升效率 |
| **📦 可追踪的源码** | `project/` 下挂载我们重点分析的项目，方便本地对照阅读和二次分析 |

**目标**：减少你到处翻 X/Twitter、Discord、HN 的时间——**只看这个仓库的更新，就能保持在前沿。**

---

## 📁 仓库结构

```
AI-ING/
├── project/          # 我们重点跟踪与分析的源码项目
│   └── clawdbot/     # 例：自托管个人 AI 助手
├── sumup/             # 项目分析产出：原理、架构、部署指南
│   └── clawdbot/      # 按项目分目录，每项目下有多份文档
│       ├── 核心技术原理.md
│       ├── 架构设计.md
│       ├── 实现细节.md
│       └── 分析与部署指南.md（若存在）
├── .cursor/skills/    # Cursor 技能（技术分析器、Code Review、Prompt 等）
├── skills/           # 与 Cursor 技能配套的可复用脚本与参考
└── README.md
```

- **`project/`**：当前重点跟踪的顶尖项目（如 clawdbot），便于本地阅读与脚本分析。
- **`sumup/`**：每个项目一个子目录，里面是**核心技术原理、架构设计、实现细节、部署指南**等文档，力求「看完就能懂、能部署」。
- **`.cursor/skills/`**、**`skills/`**：可在 Cursor 里启用的技能与配套脚本，例如用「技术分析器」自动为 `project/` 下新项目生成 `sumup/` 文档。

---

## 🎯 已覆盖 / 计划中的内容

### 项目分析（`sumup/`）

- **[Clawdbot](sumup/clawdbot-分析与部署指南.md)** — 自托管个人 AI 助手：多通道收件箱（WhatsApp / Telegram / Slack / Discord / WebChat）、本地 Gateway、语音与画布、Skills 扩展。含原理、架构与多种部署方式（npm / Docker / Fly.io / Render）。

更多项目会按「热度 + 实用性」陆续加入，每个都会在 `sumup/<项目名>/` 下产出结构化文档。

### Skills（`.cursor/skills/`、`skills/`）

- **技术分析器** — 扫描 `project/`，提取核心原理与架构，按项目名生成 `sumup/<项目名>/` 下的多份分析文档。
- **Prompt Lookup** — 提示词检索与复用。
- **Requesting / Receiving Code Review** — 发起与接收代码审查的流程与话术。
- **Skill Creator** — 从零创建新 Cursor 技能的模板与指引。

所有技能都面向「提高你日常用 AI 写码、分析项目」的效率，而不是空谈概念。

---

## 🚀 怎么用这个仓库

1. **Star & Watch**  
   在 GitHub 上 Star 并 Watch 本仓库，有新分析、新技能时在时间线里就能看到。

2. **看 `sumup/` 学项目**  
   直接打开 `sumup/<项目名>/` 下的文档，从「核心技术原理」到「部署指南」按需跳读，省掉自己啃 README + 源码的时间。

3. **在 Cursor 里用 Skills**  
   把本仓库当作你的 Cursor 工作区（或把 `.cursor/skills/` 拷贝到你的项目里），在 Cursor 设置里启用对应技能，即可用「技术分析器」分析 `project/`、用 Code Review / Prompt Lookup 等技能干活。

4. **克隆后在本地跑分析**  
   ```bash
   # 技术分析器示例：分析 project/ 下项目，输出到 sumup/<项目名>/
   python .cursor/skills/技术分析器/scripts/analyze_project.py --project-dir project/ --output-dir sumup/ --project clawdbot
   ```
   产出会按项目名落入 `sumup/<项目名>/`，便于和已有文档一起维护。

---

## 🤝 参与贡献

欢迎一起把「前沿」沉淀进这一个仓库：

- **推荐项目**：在 [Issues](https://github.com/YOUR_USERNAME/AI-ING/issues) 里用「项目推荐」模板，附上项目链接和一句「为什么值得跟进」。
- **补全 / 修正分析**：在 `sumup/<项目名>/` 下直接改对应文档，或提 PR 补充「原理 / 架构 / 部署」任一章节。
- **新增或改进 Skill**：在 `.cursor/skills/` 或 `skills/` 里提交新技能或对现有技能的改进，PR 中简要说明用法和适用场景。

参与方式与约定后续会补充到 `CONTRIBUTING.md`；在此之前欢迎直接开 [Issue](https://github.com/YOUR_USERNAME/AI-ING/issues) 讨论。

---

## 📜 许可与免责

- 本仓库中的**原创文档与技能设计**采用 MIT 许可，可自由使用与二次创作。（根目录添加 `LICENSE` 文件后即可注明具体条款。）
- `project/` 下收录的第三方项目遵循各自原仓库的许可证；本仓库仅做整理与解读，不替代官方文档与源码。

---

## 💡 为什么叫 AI-ING

**AI** 是领域，**-ING** 是进行时：前沿一直在变，这个仓库也会持续更新。  
你只需要盯着这里，就不会在「到底该看哪个」里消耗情绪——**一个项目，走在最前面。**

---

<p align="center">
  <strong>若这个仓库对你有用，请给一个 ⭐ Star</strong>
</p>

---

**发布前**：将文中 `YOUR_USERNAME` 替换为你的 GitHub 用户名；若你添加了 `LICENSE` 与 `CONTRIBUTING.md`，可相应更新文内链接。

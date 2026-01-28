# AI-ING · 一个项目，走在 AI 最前沿

> **专治 FOMO。** 只跟进这一个仓库，你就不会掉队。

[![GitHub](https://img.shields.io/badge/GitHub-xiaofuCoding--stack%2FAI--ING-24292e?logo=github)](https://github.com/xiaofuCoding-stack/AI-ING) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

大家作为程序员，日常除了写业务、修 Bug、赶需求，多少会想追一点「真·前沿」——新模型、新框架、新项目。**AI-ING** 把这个诉求收拢到一个仓库里：**精选项目深度拆解 + 拿来即用的 skill**，持续更新。你只需要 Watch 这一个 Repo。

---

## 很多人都有 FOMO，什么是 FOMO 呢？

大家作为程序员，或许都有过这种体会：一打开时间线，新模型发布、新 Agent 框架、新开源项目又上热榜了，心里会嘀咕「这个要不要跟？」又怕跟错方向白费时间，不跟又怕真香了没踩上。

我发现周围很多人都会有这种 **FOMO** 的情绪。**什么是 FOMO 呢？** 就是 *Fear Of Missing Out*，**错失恐惧**。在 AI 圈里，具体来说就是：总怕别人都在用新模型、新框架、新项目，自己还在用「上一代」；刷不完的 X、Discord、HN，越刷越慌，不知道「到底该学哪个、跟哪个」。**这种「想跟又跟不动、不跟又心痒」的状态，就是典型的 FOMO。**

这个仓库就是为了缓解这种情绪做的。把**当天最炸裂的发布、最值得跟的项目**收进 [每日前沿](sumup/每日前沿.md)，按天更新；把**已经验证过值得跟**的项目，做成「原理 + 架构 + 部署」的拆解，放在 `sumup/`。  
大家只需要：**每天扫一眼 [每日前沿](sumup/每日前沿.md)，有精力再按 `sumup/` 里的项目文档往下跟**。这样既不会漏大新闻，也不会在信息海里淹死——**一个仓库，做「前沿筛选 + 深度拆解」，专治 FOMO。**

---

## 目录

- [很多人都有 FOMO，什么是 FOMO 呢？](#很多人都有-fomo什么是-fomo-呢)
- [你会在这里得到什么](#-你会在这里得到什么)
- [每日前沿（每天最炸裂的发布）](#-每日前沿每天最炸裂的发布)
- [快速开始](#-快速开始)
- [仓库结构](#-仓库结构)
- [已覆盖内容](#-已覆盖内容)（含项目分析 + skill 清单）
- [怎么用这个仓库](#-怎么用这个仓库)
- [参与贡献](#-参与贡献)
- [许可与免责](#-许可与免责)
- [为什么叫 AI-ING](#-为什么叫-ai-ing)
- [链接](#-链接)

---

## ✨ 你会在这里得到什么

| 内容 | 说明 |
|------|------|
| **🔥 最火项目的输出** | 对热门开源项目做**原理 + 架构 + 部署**的整理，放在 `sumup/`，读完就能懂、能上手 |
| **🛠 拿来即用的 skill** | 技术分析、提示词查找、Code Review 等 skill，放进项目就能用，提升效率 |
| **📦 可追踪的源码** | `project/` 下挂我们重点分析的项目，方便本地对照阅读和二次分析 |

**目标**：少刷 X、Discord、HN——**只看这个仓库的更新，就能保持在前沿。**

---

## 📰 每日前沿（每天最炸裂的发布）

**[→ 打开「每日前沿」](sumup/每日前沿.md)**：按日更新的「当天最炸裂」发布汇总——新模型、新框架、新开源项目、重要技术动态。  

技术分析器在分析新项目或引入新技术时，会**同步把条目追加到《每日前沿》**，保证这份文档**每天更新**。你只需要每天扫一眼这一页，就知道「今天又有什么值得跟」。

---

## 🚀 快速开始

**1. 克隆仓库**

```bash
git clone https://github.com/xiaofuCoding-stack/AI-ING.git
cd AI-ING
```

**2. 打开本项目即可用 skill**

用支持 skill 的编辑器打开 `AI-ING` 目录，即可在对话里调用本仓库的 skill（技术分析器、Prompt Lookup、Code Review 等）。

**3. 本地跑技术分析器（可选）**

需 Python 3。分析 `project/` 下指定项目并输出到 `sumup/<项目名>/`：

```bash
python .cursor/skills/技术分析器/scripts/analyze_project.py --project-dir project/ --output-dir sumup/ --project clawdbot
```

---

## 📁 仓库结构

```
AI-ING/
├── project/              # 重点跟踪的源码项目
│   └── clawdbot/         # 自托管个人 AI 助手（含多通道、Gateway、skill）
├── sumup/                # 项目分析产出 + 每日前沿汇总
│   ├── 每日前沿.md        # 【每日更新】当天最炸裂的发布汇总
│   ├── clawdbot-分析与部署指南.md
│   ├── clawdbot-architecture.md
│   ├── clawdbot-core-principles.md
│   └── clawdbot-implementation.md
├── .cursor/skills/       # skill 定义（在本仓库内即生效）
│   ├── 技术分析器/       # 自动分析 project/ 并生成 sumup/
│   ├── prompt-lookup/    # 提示词检索与复用（prompts.chat MCP）
│   ├── requesting-code-review/  # 发起代码审查
│   ├── receiving-code-review/   # 接收并消化代码审查反馈
│   ├── skill-creator/   # 从零创建新 skill 的模板与指引
│   └── coolBoy/
├── skills/               # 与 skill 配套的脚本与参考（可单独复用）
│   └── tech-analyzer/   # 技术分析器英文版 + 分析模式参考
└── README.md
```

- **`project/`**：重点跟踪的顶尖项目，便于本地阅读与脚本分析。
- **`sumup/`**：各项目的**核心技术原理、架构设计、实现细节、部署指南**等文档。
- **`.cursor/skills/`**：skill 定义目录；用本仓库作工作区即可使用这些 skill。
- **`skills/`**：可拷贝到其他项目或单独引用的脚本与参考。

---

## 🎯 已覆盖内容

### 项目分析（`sumup/`）

| 项目 | 文档 | 说明 |
|------|------|------|
| **Clawdbot** | [分析与部署指南](sumup/clawdbot-分析与部署指南.md) | 自托管个人 AI 助手：多通道收件箱、本地 Gateway、语音与画布、skill。含 npm / Docker / Fly.io / Render 部署 |
| | [架构设计](sumup/clawdbot-architecture.md) | 系统架构、组件、数据流、扩展点、通信模式 |
| | [核心原理](sumup/clawdbot-core-principles.md) | 设计原则、关键抽象、架构模式 |
| | [实现细节](sumup/clawdbot-implementation.md) | 技术栈、依赖、实现与构建部署 |

更多项目会按「热度 + 实用性」陆续加入，并在 `sumup/` 下产出结构化文档。

### skill（`.cursor/skills/`、`skills/`）

| 技能 | 路径 | 说明 |
|------|------|------|
| **技术分析器** | `.cursor/skills/技术分析器/` | 扫描 `project/`，提取核心原理与架构，按项目名生成 `sumup/<项目名>/` 下的多份分析文档 |
| **Prompt Lookup** | `.cursor/skills/prompt-lookup/` | 通过 prompts.chat MCP 检索、获取、优化提示词模板 |
| **Requesting Code Review** | `.cursor/skills/requesting-code-review/` | 在完成任务、实现大功能、合并前发起代码审查 |
| **Receiving Code Review** | `.cursor/skills/receiving-code-review/` | 接收审查反馈时先理解再落实，强调验证与技术正确性 |
| **Skill Creator** | `.cursor/skills/skill-creator/` | 从零创建新 skill 的模板与指引 |
| **tech-analyzer（英文）** | `skills/tech-analyzer/` | 技术分析器英文版及分析模式参考，可单独复用 |

这些 skill 都面向「提高日常用 AI 写码、分析项目」的效率。

---

## 🚀 怎么用这个仓库

1. **Star & Watch**  
   在 GitHub 上 [Star](https://github.com/xiaofuCoding-stack/AI-ING) 并 Watch 本仓库，有新分析、新 skill 时在时间线里就能看到。

2. **每天扫一眼《每日前沿》**  
   打开 [sumup/每日前沿.md](sumup/每日前沿.md)，按日查看「当天最炸裂的发布」汇总，不漏大新闻。

3. **看 `sumup/` 学项目**  
   从 [sumup/clawdbot-分析与部署指南.md](sumup/clawdbot-分析与部署指南.md) 等文档入手，按「原理 → 架构 → 部署」跳读，省掉自己啃 README + 源码的时间。

4. **用本仓库里的 skill**  
   克隆后用支持 skill 的编辑器打开本仓库（或把 `.cursor/skills/` 下的技能目录拷贝到你的项目里），启用对应 skill，即可用「技术分析器」分析 `project/`、用 Code Review / Prompt Lookup 等干活。

5. **克隆后在本地跑分析**  
   见上方 [快速开始](#-快速开始) 中的分析器命令；产出会按项目名落入 `sumup/<项目名>/`，便于和已有文档一起维护。

---

## 🤝 参与贡献

欢迎一起把「前沿」沉淀进这一个仓库：

- **推荐项目**：在 [Issues](https://github.com/xiaofuCoding-stack/AI-ING/issues) 里说明项目链接和「为什么值得跟进」。
- **补全 / 修正分析**：在 `sumup/` 下直接改对应文档，或提 PR 补充「原理 / 架构 / 部署」任一章节。
- **新增或改进 skill**：在 `.cursor/skills/` 或 `skills/` 里提交新 skill 或对现有 skill 的改进，PR 中简要说明用法和适用场景。

参与方式与约定后续会补充到 `CONTRIBUTING.md`；在此之前欢迎直接开 [Issue](https://github.com/xiaofuCoding-stack/AI-ING/issues) 讨论。

---

## 📜 许可与免责

- 本仓库中的**原创文档与 skill 设计**采用 MIT 许可，可自由使用与二次创作。若在根目录添加 `LICENSE` 文件，则以该文件为准。
- `project/` 下收录的第三方项目遵循各自原仓库的许可证；本仓库仅做整理与解读，不替代官方文档与源码。

---

## 💡 为什么叫 AI-ING

**AI** 是领域，**-ING** 是进行时：前沿一直在变，这个仓库也会持续更新。  
你只需要盯着这里，就不会在「到底该看哪个」里消耗情绪——**一个项目，走在最前面。**

---

## 🔗 链接

| 链接 | 地址 |
|------|------|
| **仓库** | [github.com/xiaofuCoding-stack/AI-ING](https://github.com/xiaofuCoding-stack/AI-ING) |
| **Issues** | [Issues](https://github.com/xiaofuCoding-stack/AI-ING/issues) |
| **克隆** | `git clone https://github.com/xiaofuCoding-stack/AI-ING.git` |

若这个仓库对你有用，请给一个 ⭐ [Star](https://github.com/xiaofuCoding-stack/AI-ING)。

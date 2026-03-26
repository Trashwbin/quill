---
title: "CLI vs MCP vs Skills：整个争论都问错了问题"
date: 2026-03-26
draft: false
tags: ["AI Agent", "MCP", "CLI", "Skills", "OAuth"]
summary: "2026 年 AI Agent 社区最热的架构之争。CLI 派说 MCP 浪费 token，MCP 派说标准化才是未来，Skills 派说一个 Markdown 就够了。但做过 MCP Server 之后，我发现整个争论都在回避真正的问题。"
mermaid: true
---

## 他们在吵什么

2026 年 3 月，AI Agent 圈最热的话题不是哪个模型更强，而是一个听起来很无聊的架构问题：

> Agent 该用什么方式调用外部工具？

三个阵营打得不可开交：

**MCP 派**（Model Context Protocol）：Anthropic 2024 年底推出的开放标准。通过 JSON-RPC 协议统一封装各类服务接口，Agent 一次接入就能跨平台调用多种工具。OpenAI、Google、Microsoft、AWS 全部跟进。听起来很美好。

**CLI 派**：直接让 Agent 跑 shell 命令——`git log`、`gh pr list`、`curl`、`kubectl`。不需要任何协议层，不需要额外服务器。50 年前的 `grep` 和 `awk` 在 AI 时代焕发第二春。

**Skills 派**：一个 Markdown 文件当"小抄"，教 Agent 在什么场景用什么工具。30 token 待命，触发时才加载完整指令。Flask 作者 Armin Ronacher 全面转向这个方案。

## 最新战况（吃瓜指南）

MCP 正在被"退货"：

- Perplexity 发博客宣布准备全面抛弃 MCP 转向 CLI
- 开发者吐槽："MCP 就像给自行车装火箭推进器，太重了"
- 19 万 star 的 Agent 框架作者直接说 "MCP was a mistake"
- **连 MCP 的"亲爹" Anthropic，自家的 Claude Code 也更像 CLI 而非 MCP**

CLI 的"文艺复兴"：

- Andrej Karpathy 2026 年 2 月说 CLI "super exciting precisely because they are legacy"
- GitHub 上最火的项目从"MCP 工具"变成"AI 命令行助手"
- Google 专门开源了给 AI 用的命令行工具

Skills 的悄然崛起：

- Armin Ronacher 全面从 MCP 转向 Skills
- OpenCode / Claude Code 的 Skills 体系越来越成熟
- 社区开始出现"删掉所有 MCP，用 Skills + CLI 替代"的实践文章

## CLI 赢在哪？技术层面拆解

### 1. MCP 的上下文污染

MCP 最大的问题：**Agent 一启动就要把所有工具的 schema 塞进上下文。**

GitHub 的 MCP Server 暴露 43 个工具，连接它就往上下文注入约 55,000 token 的工具定义。还没开始干活，token 预算花掉一大半。接 10 个 MCP Server、100 个工具？上下文直接爆炸。

CLI 完全不同——**渐进式发现**。Agent 先跑 `gh --help` 看有什么命令，需要时再 `gh pr --help` 看子命令参数。信息按需加载，不是开局全塞。

### 2. LLM 天然会用 CLI

LLM 训练数据里有几十年的 Unix 文档、Stack Overflow 回答、GitHub 上的 shell 脚本。模型天生认识 `git`、`curl`、`grep`、`docker`。

MCP 呢？大量的 JSON schema，模型更难处理，还要输出格式化的 JSON token。你自定义的 MCP 工具，模型从训练数据里学不到怎么调。

### 3. 管道操作

MCP 工具返回结果如果需要后处理（过滤、搜索、截取），得写额外代码。CLI 直接 pipe：

```bash
gh pr list --json number,title | jq '.[] | select(.title | contains("fix"))'
```

Agent 输出几个命令用 `|` 连起来，后处理就搞定了。更简单、更灵活、维护成本更低。

### 4. CLI + Skills 天然搭配

Skill 文件里教 Agent 用 CLI，干净利落：

```markdown
## 查看 PR 状态
gh pr list --state open --json number,title,author
```

换成 MCP？Skill 文件会充斥 function call、JSON schema，整个文档混乱不堪。

### 数据说话

ScaleKit 75 次基准测试，同一个 GitHub 任务：

```mermaid
graph LR
    subgraph Token 消耗对比
        CLI["CLI<br/>1,365 tokens"]
        Skills["CLI + Skills<br/>4,724 tokens"]
        MCP["MCP<br/>44,026 tokens"]
    end
    
    CLI -->|"3.5x"| Skills
    Skills -->|"9.3x"| MCP
    CLI -->|"32x"| MCP
    
    style CLI fill:#22c55e,color:#fff
    style Skills fill:#eab308,color:#fff
    style MCP fill:#ef4444,color:#fff
```

| 方案 | 月成本（1 万次） | 可靠性 |
|------|-----------------|--------|
| CLI | ~$3.20 | 100% |
| CLI + Skills | ~$4.50 | 100% |
| MCP | ~$55.20 | 72%（28% 超时） |

CLI 便宜 17 倍，可靠性 100% vs 72%。碾压。

## 到这里，CLI 似乎完胜

Token 更省、模型更熟悉、可以 pipe、跟 Skills 搭配更好。各个维度 MCP 都被吊打。

**如果故事到这里结束，那 MCP 就是一个失败的协议，CLI 是唯一的答案。**

但这个结论有一个致命前提——**所有基准测试都在同一个场景下跑：一个开发者，用自己的凭证，自动化自己的工作流。**

很多文章写到这就会说："但 MCP 有 OAuth，多租户场景不可替代！CLI 做不了认证！"

**真的吗？**

## 一个来自今天的亲身体验

我今天用 OpenCode（CLI 形式的 AI Agent）部署了这个博客。Agent 调了 Vercel CLI：

```bash
$ vercel login
→ 自动弹出浏览器 OAuth 页面
→ 点一下授权
→ CLI 自动拿到 token，本地保存
→ 之后所有命令无感使用
```

**十秒钟。一个 CLI 工具，完整跑了 OAuth 浏览器授权流程。**

我又想到 `gh auth login`——GitHub CLI 也是一模一样。弹出浏览器，OAuth 授权，scoped token，本地持久化。

所以：

> **CLI 不是"架构上不支持 OAuth"。`gh` 和 `vercel` 已经证明了。**

如果微信愿意做一个 `wx auth login`，流程跟 `gh` 一模一样：

```bash
$ wx auth login
→ 弹出微信扫码页面
→ 手机确认授权
→ 本地保存 token
→ wx send abin "你好"
→ wx moments list
```

**技术上零障碍。但它永远不会出现。**

不是做不到，是做了等于把苦苦经营的生态壁垒和反爬体系直接关掉。

## 那 MCP 到底有什么用？

MCP 的价值不是"做了 CLI 做不了的事"——`gh` 已经证明 CLI 能做 OAuth。

MCP 的价值是**标准化**：

```mermaid
graph TB
    subgraph "没有 MCP 的世界"
        P1["GitHub: gh auth login"]
        P2["Vercel: vercel login"]
        P3["AWS: aws configure"]
        P4["平台 N: 又一套新的"]
    end
    
    subgraph "有 MCP 的世界"
        MCP_std["统一的 OAuth 发现协议<br/>统一的工具 schema<br/>统一的调用方式"]
    end
    
    style MCP_std fill:#6366f1,color:#fff
```

接 1 个平台，`gh` 就够了。接 50 个平台，每个都搞一套 CLI auth 就崩溃了。MCP 提供了"大家都用同一套协议开放"的可能性。

**但标准化有个前提：平台愿意实现它。**

## 所以整个争论都问错了问题

```mermaid
graph TB
    subgraph "社区在争的"
        Debate["CLI vs MCP 哪个更好？"]
    end
    
    subgraph "应该问的"
        Real["平台愿不愿意开放数据？"]
    end
    
    Debate --> Solved["已经有答案<br/>CLI 更高效 / MCP 更标准 / Skills 更轻量"]
    Real --> Unsolved["没有答案<br/>微信不做 wx CLI<br/>淘宝不开放比价 API<br/>美团不给评分数据"]
    
    style Debate fill:#94a3b8,color:#fff
    style Real fill:#ef4444,color:#fff
    style Solved fill:#22c55e20,stroke:#22c55e
    style Unsolved fill:#ef444420,stroke:#ef4444
```

GitHub 做了 `gh` → CLI 碾压一切。
Vercel 做了 `vercel login` → 部署丝滑无比。
微信没做 `wx` → 你只能爬虫，或者等。

**决定 Agent 能力边界的，不是你选了 CLI 还是 MCP，而是平台愿不愿意给你一根管道——不管什么形式的管道。**

CLI vs MCP 争的是管道的材质。**真正缺的是水龙头。**

Token 成本是工程问题，协议选择是架构问题，**数据开放是政治问题。** 前两个正在被解决，第三个才是真正卡住整个 Agent 生态的瓶颈。而整个社区都在用技术问题的框架，回避那个真正难的政治问题。

---

*这是 "Agent 生态思考" 系列第一篇。下一篇聊：就算平台有 API，你也大概率用不了——Agent 落地的三层壁垒比你想的厚得多。*

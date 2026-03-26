---
title: "我用一条命令部署了博客，然后想到了微信"
date: 2026-03-26
draft: false
tags: ["AI Agent", "MCP", "CLI", "Skills", "OAuth"]
summary: "vercel login 十秒完成 OAuth，gh auth login 也是。技术上 wx auth login 一样能做。但它永远不会出现。CLI vs MCP 的争论问错了问题——瓶颈不是协议，是水龙头愿不愿意打开。"
mermaid: true
---

## 从一次部署说起

今天我用 OpenCode（一个 CLI 形式的 AI Agent）部署这个博客。过程中它调用了 Vercel CLI：

```bash
$ vercel login
→ 自动打开浏览器 OAuth 页面
→ 点一下授权
→ CLI 自动拿到 token
→ 后续所有操作无感

$ vercel --prod
→ 构建、上传、部署，一气呵成
```

整个 auth 流程十秒钟。我甚至没意识到它发生了。

这让我想到 `gh auth login`——GitHub 的 CLI 也是同样的体验。弹出浏览器，OAuth 授权，本地保存 token，之后 `gh pr create`、`gh repo clone` 随便用。

然后我想：如果微信也有一个 `wx auth login` 呢？

```bash
$ wx auth login
→ 弹出微信扫码页面
→ 手机确认授权
→ 本地保存 token
→ wx send abin "你好"
→ wx moments list
→ wx pay transfer ...
```

**技术上，跟 `vercel login` 和 `gh auth login` 一模一样。** 没有任何技术障碍。

但它永远不会出现。

## 2026 年最热的技术争论

AI Agent 社区今年最火的话题：Agent 该用什么方式调用外部工具？

三个阵营：

- **CLI 派**：直接跑 shell 命令，`git`、`gh`、`curl`，LLM 训练数据里就有，便宜、快、可靠
- **MCP 派**：Anthropic 推出的标准协议，JSON schema + OAuth，大厂全部跟进
- **Skills 派**：一个 Markdown 文件当"小抄"，教 Agent 怎么用工具，30 token 待命

ScaleKit 做了 75 次基准测试，同一个 GitHub 任务：

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
| MCP | ~$55.20 | 72% |

CLI 阵营的结论：MCP 就是浪费钱。Andrej Karpathy 说 CLI "super exciting"，19 万 star 的 Agent 框架作者说 "MCP was a mistake"，Flask 作者全面转向 Skills。

MCP 完败？

## 但这个比较有一个致命前提

**所有基准测试都在同一个场景下跑：一个开发者，用自己的凭证，自动化自己的工作流。**

```mermaid
graph TB
    subgraph "基准测试的场景"
        Dev["你（已登录 gh）"]
        Agent["Agent"]
        GitHub["GitHub API"]
        
        Dev -->|"凭证已有"| Agent
        Agent -->|"gh pr list"| GitHub
        GitHub -->|"返回数据"| Agent
    end
    
    subgraph "多用户场景"
        User["用户 A / B / C..."]
        Agent2["Agent（SaaS 产品）"]
        Platform["第三方平台"]
        
        User -->|"各自的 OAuth"| Agent2
        Agent2 -->|"scoped token"| Platform
        Platform -->|"只返回该用户的数据"| Agent2
    end
    
    style Dev fill:#6366f1,color:#fff
    style User fill:#6366f1,color:#fff
    style Agent fill:#a855f7,color:#fff
    style Agent2 fill:#a855f7,color:#fff
```

在左边的场景里，CLI 赢得毫无悬念。在右边——你需要多用户 OAuth、权限隔离、审计日志。

很多文章写到这里就会说："所以 MCP 不可替代。"

**但这是错的。**

## `gh` 就是反例

回到开头的体验。`gh auth login` 做了什么？

1. 发起 OAuth 浏览器授权
2. 用户确认，拿到 scoped token
3. 本地持久化登录态
4. 后续所有命令自动带 token

这是一个 **CLI 工具完整实现了 OAuth 授权流程**。

`vercel login` 也是。我今天亲手体验了——Agent 调用 Vercel CLI，OAuth 在浏览器里完成，整个过程对 Agent 来说完全透明。

所以 CLI 不是"架构上不支持 OAuth"，而是**大多数平台根本没有提供 CLI**。GitHub 做了 `gh`，CLI 就碾压 MCP。微信没做 `wx`，你只能走 MCP 或者爬虫。

那 MCP 的价值到底是什么？

## MCP 的真正价值：不是不可替代，是标准化

```mermaid
graph TB
    subgraph "没有 MCP 的世界"
        P1["GitHub: gh auth login"]
        P2["Vercel: vercel login"]
        P3["AWS: aws configure"]
        P4["平台 N: ???"]
        
        P1 --> Different1["各自的 auth 流程"]
        P2 --> Different2["各自的 token 格式"]
        P3 --> Different3["各自的 scope 命名"]
        P4 --> Different4["又一套新的"]
    end
    
    subgraph "有 MCP 的世界"
        MCP_std["MCP 标准协议"]
        MCP_std --> Unified1["统一的 OAuth 发现<br/>/.well-known/oauth-authorization-server"]
        MCP_std --> Unified2["统一的工具 schema"]
        MCP_std --> Unified3["统一的调用方式"]
    end
    
    style MCP_std fill:#6366f1,color:#fff
```

当你只接 GitHub，`gh` 就够了。当你要接 50 个平台，每个都搞一套 CLI auth 流程就崩溃了。MCP 的价值是**"大家都用同一套协议开放"**——是标准化，不是不可替代。

**但标准化有个前提：平台愿意实现它。**

## 三个方案，三个层面

```mermaid
graph TB
    subgraph "三层问题"
        L1["怎么调？<br/>（执行效率）"]
        L2["怎么教 Agent 调？<br/>（知识传递）"]
        L3["谁愿意被调？<br/>（数据开放）"]
    end
    
    L1 --- CLI_sol["CLI 最优<br/>200 tokens/次<br/>LLM 天然会用"]
    L2 --- Skills_sol["Skills 最优<br/>按需加载<br/>30 tokens 待命"]
    L3 --- Open_sol["需要平台配合<br/>CLI 或 MCP 都行<br/>关键是平台愿不愿意做"]
    
    L1 --> L2 --> L3
    
    style L1 fill:#22c55e,color:#fff
    style L2 fill:#eab308,color:#fff
    style L3 fill:#ef4444,color:#fff
    style CLI_sol fill:#22c55e20,stroke:#22c55e
    style Skills_sol fill:#eab30820,stroke:#eab308
    style Open_sol fill:#ef444420,stroke:#ef4444
```

第一层和第二层是技术问题，基本已经解决了。

**第三层不是技术问题。** `gh` 证明了 CLI 能做 OAuth。MCP 提供了标准化方案。技术全部就绪。

**缺的是水龙头，不是管道。**

## 所以整个争论都问错了问题

```mermaid
flowchart TD
    Wrong["社区在问的问题<br/>'CLI 还是 MCP 更好？'"]
    Right["应该问的问题<br/>'平台愿不愿意开放数据？'"]
    
    Wrong -->|"技术层面"| Tech["已经有答案了<br/>CLI 高效 / MCP 标准 / Skills 轻量<br/>按场景选就行"]
    Right -->|"政治层面"| Politics["没有答案<br/>涉及平台商业模式的根基"]
    
    Tech --> Solved["✅ 工程问题，正在被解决"]
    Politics --> Unsolved["❌ 博弈问题，才刚开始"]
    
    style Wrong fill:#ef4444,color:#fff
    style Right fill:#22c55e,color:#fff
    style Solved fill:#22c55e20,stroke:#22c55e
    style Unsolved fill:#ef444420,stroke:#ef4444
```

我今天部署博客时 `vercel login` 的体验，跟 `gh auth login` 一样丝滑。如果 `wx auth login` 也能这样——

```bash
$ wx auth login
→ 弹出微信扫码
→ 确认授权
→ wx send abin "你好"
```

——那 Agent 立刻就能帮你发消息、管朋友圈、处理微信支付。技术上没有任何障碍。

**但微信不会做。** 不是做不到，是做了等于把苦苦经营的生态壁垒和反爬体系直接关掉。

Token 成本是工程问题，协议选择是架构问题，**数据开放是政治问题。** 前两个正在被解决，第三个才是真正卡住 Agent 生态的瓶颈。

而整个社区都在用技术问题的框架，回避那个真正难的政治问题。

---

*这是 "Agent 生态思考" 系列第一篇。下一篇聊聊：就算平台有 API，你也大概率用不了——Agent 落地的三层壁垒远比你想的厚。*

---
title: "Agent 的瓶颈不是 AI，是数据主权"
date: 2026-03-26
draft: false
tags: ["AI Agent", "数据主权", "平台生态", "阿里巴巴"]
summary: "LLM 够聪明了，CLI 够高效了，MCP 够标准了。但你的 Agent 依然帮不了你什么忙。不是因为技术不行，是因为数据拿不出来。"
mermaid: true
---


> LLM 够聪明了，CLI 够高效了，MCP 够标准了。但你的 Agent 依然帮不了你什么忙。不是因为技术不行，是因为数据拿不出来。这篇文章聊的不是技术架构，是 Agent 生态真正的卡脖子问题。

## 一个思想实验

假设现在有一个完美的 Agent：

- 推理能力顶级（Claude Opus / GPT-5 级别）
- 工具调用零延迟（CLI + MCP 混合架构）
- 上下文无限（不存在 token 限制）

你跟它说："帮我规划下周末带家人去杭州玩两天，预算 3000，我妈腿不好别走太多路。"

它需要什么？

```mermaid
graph TB
    Request["帮我规划杭州周末游<br/>预算3000，老人腿不好"]
    
    Request --> Need1["交通信息<br/>高铁/机票比价"]
    Request --> Need2["酒店推荐<br/>适合老人的无障碍酒店"]
    Request --> Need3["景点路线<br/>步行距离短的方案"]
    Request --> Need4["餐厅推荐<br/>适合老人口味"]
    Request --> Need5["健康数据<br/>老人的身体状况"]
    Request --> Need6["支付<br/>统一预订和付款"]
    
    Need1 -->|"12306 / 携程"| Block1["❌ 不开放"]
    Need2 -->|"携程 / 美团"| Block2["❌ 不开放"]
    Need3 -->|"高德地图"| Block3["⚠️ 部分开放"]
    Need4 -->|"大众点评"| Block4["❌ 不开放"]
    Need5 -->|"健康 App"| Block5["❌ 不开放"]
    Need6 -->|"支付宝/微信支付"| Block6["❌ 不开放"]
    
    style Request fill:#6366f1,color:#fff
    style Block1 fill:#ef4444,color:#fff
    style Block2 fill:#ef4444,color:#fff
    style Block3 fill:#eab308,color:#fff
    style Block4 fill:#ef4444,color:#fff
    style Block5 fill:#ef4444,color:#fff
    style Block6 fill:#ef4444,color:#fff
```

6 个数据源，5 个完全不开放，1 个部分开放。

**Agent 的能力被截断在数据入口。** 不是不够聪明，是根本拿不到做决策需要的信息。

## Agent 能力公式

```mermaid
graph LR
    subgraph "Agent 的真实能力"
        A["LLM 推理"] 
        B["工具调用"]
        C["可访问的数据"]
    end
    
    A -->|"✅ 已解决"| Score1["10/10"]
    B -->|"✅ 基本解决"| Score2["8/10"]
    C -->|"❌ 严重不足"| Score3["2/10"]
    
    Result["Agent 实际能力 = 10 × 8 × 2 = 160 / 1000"]
    
    Score1 --> Result
    Score2 --> Result
    Score3 --> Result
    
    style Score1 fill:#22c55e,color:#fff
    style Score2 fill:#22c55e,color:#fff
    style Score3 fill:#ef4444,color:#fff
    style Result fill:#f97316,color:#fff
```

**整个行业在卷 LLM 能力和工具协议，但真正的短板是数据访问。** 这就像你有一辆法拉利和一条完美的赛道，但油箱是空的。

## 为什么数据拿不出来？

### 不是技术问题，是商业模式问题

```mermaid
graph TB
    subgraph "平台的商业逻辑"
        Data["用户数据<br/>（行为、偏好、社交关系）"]
        Data --> Ads["精准广告<br/>核心营收"]
        Data --> Lock["用户锁定<br/>迁移成本"]
        Data --> Decision["操纵决策<br/>推荐算法"]
    end
    
    subgraph "Agent 的威胁"
        Agent["用户的 Agent"]
        Agent -->|"跨平台比价"| Threat1["打破信息茧房"]
        Agent -->|"最优决策"| Threat2["用户不再被引导消费"]
        Agent -->|"数据可携带"| Threat3["迁移成本归零"]
    end
    
    Threat1 -.->|"直接威胁"| Ads
    Threat2 -.->|"直接威胁"| Decision
    Threat3 -.->|"直接威胁"| Lock
    
    style Data fill:#6366f1,color:#fff
    style Agent fill:#a855f7,color:#fff
    style Threat1 fill:#ef4444,color:#fff
    style Threat2 fill:#ef4444,color:#fff
    style Threat3 fill:#ef4444,color:#fff
```

**Agent 对民生的价值和对平台利润的威胁，是同一件事的两面。**

当 Agent 能帮用户做最优选择时，平台就失去了操纵用户决策的能力。而这恰恰是大多数平台最大的利润来源。

所以微信不会做 `wx send` CLI，淘宝不会让你的 Agent 比价，美团不会开放商家评分的原始数据。不是技术做不到，是做了会动摇商业根基。

## GitHub 模式 vs 微信模式

有些平台开放了，有些没有。差别在哪？

```mermaid
graph TB
    subgraph "GitHub 模式 ✅"
        GH_Model["商业模式：卖服务（订阅）"]
        GH_Model --> GH_Logic["开放数据 → 生态繁荣<br/>→ 更多人用 GitHub<br/>→ 更多付费订阅"]
        GH_Logic --> GH_Result["gh auth login ✅<br/>完整 CLI + OAuth"]
    end
    
    subgraph "微信模式 ❌"
        WX_Model["商业模式：卖流量（广告）"]
        WX_Model --> WX_Logic["开放数据 → 用户绕过平台<br/>→ 广告价值下降<br/>→ 核心营收受损"]
        WX_Logic --> WX_Result["wx auth login ❌<br/>反爬 + 封号"]
    end
    
    style GH_Model fill:#22c55e,color:#fff
    style WX_Model fill:#ef4444,color:#fff
    style GH_Result fill:#22c55e,color:#fff
    style WX_Result fill:#ef4444,color:#fff
```

| 平台类型 | 代表 | 对 Agent 开放？ | 原因 |
|---------|------|----------------|------|
| 卖服务的 | GitHub, Notion, Linear, Vercel | ✅ 主动开放 | 开放 = 更多用户 = 更多订阅 |
| 卖流量的 | 微信, 淘宝, 抖音, 美团 | ❌ 封锁 | 开放 = 用户绕过推荐 = 广告贬值 |
| 卖企业服务的 | 飞书, 钉钉, 企微 | ⚠️ 有限开放 | 开放 Bot API = 企业更依赖平台 |

**一个平台会不会开放数据给 Agent，取决于开放是否符合它的商业利益。** 技术标准（MCP 也好，CLI 也好）只是管道，管道再好，水龙头不开也没用。

## 私有生态闭环：阿里的路径

在跨平台开放看不到希望的情况下，有人选择了另一条路：**在自己的围墙里先把闭环做了。**

```mermaid
graph TB
    subgraph "阿里生态闭环"
        User["用户（一个支付宝账号）"]
        
        User --> TB["淘宝/天猫<br/>想买东西"]
        User --> GD["高德地图<br/>想出门"]
        User --> FZ["飞猪<br/>想旅行"]
        User --> ZFB["支付宝<br/>想付钱"]
        User --> MF["蚂蚁理财<br/>想理财"]
        User --> ELM["饿了么<br/>想吃饭"]
        User --> Health["阿里健康<br/>看病"]
    end
    
    subgraph "Agent 可以做"
        Agent["阿里 Agent<br/>一个账号打通所有数据"]
        Agent -.-> TB
        Agent -.-> GD
        Agent -.-> FZ
        Agent -.-> ZFB
        Agent -.-> ELM
        Agent -.-> Health
    end
    
    style User fill:#6366f1,color:#fff
    style Agent fill:#a855f7,color:#fff
```

阿里手上的牌恰好覆盖了一个人日常生活的完整链路。一个 Agent 只接阿里系的数据，就已经能回答那个杭州旅行的问题——高德知道路线和步行距离，飞猪知道酒店，淘宝能买装备，支付宝能付钱，健康数据知道老人身体状况。

**Auth 问题天然解决了——你已经登录了支付宝，整个阿里系共享一套账号体系。**

### 但这里面有个微妙的问题

```mermaid
graph LR
    subgraph "用户想要的"
        U["Agent 帮我做最优决策"]
    end
    
    subgraph "阿里想要的"
        A["Agent 帮你做决策<br/>但只在阿里生态里"]
    end
    
    U -->|"方向一致"| Common["都希望 Agent 能干活"]
    A -->|"目的不同"| Hidden["不会告诉你携程更便宜"]
    
    style U fill:#22c55e,color:#fff
    style A fill:#f97316,color:#fff
    style Hidden fill:#ef4444,color:#fff
```

阿里的 Agent 帮你在飞猪订了酒店，但它不会告诉你携程同一家店便宜 200 块。帮你在淘宝下了单，但不会告诉你拼多多有更低价。

**私有生态 Agent 的本质是：用 AI 的便利性换取用户对比价权的放弃。**

## 那些"绕路"的尝试

等不及平台开放，有人开始用技术手段强行突破：

```mermaid
graph TB
    subgraph "绕路方案"
        D1["豆包手机<br/>屏幕级 RPA"]
        D2["OpenCLI / CLI Anything<br/>逆向 API 封装"]
        D3["各种 Agent 框架<br/>封装调用链"]
    end
    
    D1 --> Nature1["本质：模拟人点屏幕"]
    D2 --> Nature2["本质：反爬 / 逆向工程"]
    D3 --> Nature3["本质：谁有 API 我接谁"]
    
    Nature1 --> Problem["共同问题"]
    Nature2 --> Problem
    Nature3 --> Problem
    
    Problem --> P1["脆弱 — UI 改版就废"]
    Problem --> P2["灰色地带 — 随时被封"]
    Problem --> P3["没有真正获得数据结构"]
    
    style D1 fill:#6366f1,color:#fff
    style D2 fill:#6366f1,color:#fff
    style D3 fill:#6366f1,color:#fff
    style Problem fill:#ef4444,color:#fff
```

这些产品确实在推动一件对的事——让 Agent 真正帮到用户。但用的是一种注定不可持续的方式。

就像早期的视频网站靠盗版起量——用户确实获益了，但这个模式不可能长久。

## Agent 生态的演进阶段

```mermaid
graph LR
    S1["阶段一<br/>野蛮生长"]
    S2["阶段二<br/>灰色博弈"]
    S3["阶段三<br/>正规化"]
    S4["阶段四<br/>成熟期"]
    
    S1 -->|"现在在这"| S2
    S2 --> S3
    S3 --> S4
    
    S1 --- D1["爬虫 / RPA / 逆向 API"]
    S2 --- D2["平台封杀 vs 用户需求"]
    S3 --- D3["OAuth 授权 / MCP 标准化"]
    S4 --- D4["标准化数据开放"]
    
    S1_ex["类比：盗版视频网站"]
    S2_ex["类比：版权纠纷期"]
    S3_ex["类比：版权采购 + 自制"]
    S4_ex["类比：Netflix"]
    
    S1 --- S1_ex
    S2 --- S2_ex
    S3 --- S3_ex
    S4 --- S4_ex
    
    style S1 fill:#ef4444,color:#fff
    style S2 fill:#f97316,color:#fff
    style S3 fill:#eab308,color:#fff
    style S4 fill:#22c55e,color:#fff
```

我们大概在第一到第二阶段之间。

## 什么会���正推动变化？

技术不会。推动变化的是三件事：

### 1. 用户预期

当足够多的用户习惯了"跟 Agent 说一句话就能办事"，回不去手动操作了，平台就必须响应。阿里如果率先做出好用的闭环 Agent，其他平台的用户体验落差会变得不可忍受。

### 2. 监管压力

欧盟 DMA（数字市场法案）已经在强制大平台开放互操作。国内的《个人信息保护法》有数据可携带条款，但执行力度未知。如果出台类似政策并认真执行，这就是真正的转折点。

### 3. 竞争的囚徒困境

```mermaid
graph TB
    subgraph "囚徒困境"
        Ali["阿里做出闭环 Agent<br/>用户体验领先"]
        
        Ali --> Choice["其他厂商的选择"]
        
        Choice -->|"方案 A"| A["自己也做闭环<br/>成本极高，生态不够"]
        Choice -->|"方案 B"| B["接入开放协议<br/>成本低，但要开放数据"]
        Choice -->|"方案 C"| C["什么都不做<br/>用户流失"]
    end
    
    B --> Result["当 B 成为多数选择时<br/>MCP 等标准协议才真正被需要"]
    
    style Ali fill:#6366f1,color:#fff
    style B fill:#22c55e,color:#fff
    style C fill:#ef4444,color:#fff
    style Result fill:#a855f7,color:#fff
```

就像当年银联/网联打通支付——不是谁主动想开放，是监管 + 竞争 + 用户预期共同推动的。

## 结论

> **AIGC 时代的瓶颈不是 AI 不够强，是数据持有者没有动力让 AI 替用户做选择。**

因为一旦 Agent 能帮用户做最优选择，平台就失去了操纵用户决策的能力——而这恰恰是它们最大的利润来源。

Token 成本是工程问题，CLI vs MCP 是架构问题，**数据开放是政治问题**。前两个正在被解决，第三个才刚刚开始被意识到。

下一次当你看到有人在争论 "MCP 浪费 token" 或 "CLI 不安全" 时，想一想：就算这些问题全解决了，你的 Agent 能帮你做什么？

**答案取决于数据的主人愿不愿意开门。** 而这个问题，不在任何技术规范的讨论范围内。

---

*这是 "Agent 生态思考" 系列的第二篇。下一篇聊一个更隐蔽的问题：为什么你在浏览器里能看到的数据，Agent 依然拿不到。*

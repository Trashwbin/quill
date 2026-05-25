---
name: quill-ecosystem-analysis
version: 1.0.0
description: "Write and edit Quill ecosystem analysis posts: AI Agent industry structure, platform incentives, product categories, CLI/MCP/Skills debates, permissions, data access, organization constraints, and harness competition."
---

# Quill Ecosystem Analysis

Use this skill for product, platform, market, and ecosystem analysis posts. Do not use it for code-first implementation posts unless the technical design is inseparable from platform incentives or permission boundaries.

## Positioning

These posts are not product reviews or news summaries. They are structured arguments about why an ecosystem behaves the way it does.

The main promise is:

> 从一个表面争论里，拆出真正的结构性约束。

## Voice

- Write like a systems-minded programmer analyzing industry structure.
- Prefer clear judgment over neutral summary.
- Be technically optimistic but not naive.
- Treat incentives, permissions, data access, organization approval, reliability, and user experience as first-class constraints.
- Avoid hype, promotional framing, vague futurism, and empty "both sides" balance.

## Core Thesis Pattern

Most posts should move from a visible debate to the real bottleneck:

1. Start with a current dispute, product claim, or realistic user scenario.
2. State why the common framing is wrong or incomplete.
3. Split the problem into concrete layers, variables, strategies, or tradeoffs.
4. Use examples, tables, and Mermaid diagrams to make the structure inspectable.
5. End with a compact conclusion that can be remembered as one sentence.

Typical claim shapes:

- "不是 A，而是 B。"
- "X 是工程问题，Y 是架构问题，Z 才是真正的瓶颈。"
- "技术上可行，不等于现实中可用。"
- "这个问题没有纯技术解。"

## Default Structure

```markdown
## 一个常见说法 / 一个真实场景

Describe the industry narrative, demo promise, or concrete workflow.

## 真正的问题不是 X

Name the hidden constraint and state the thesis early.

## 拆成 N 个变量 / N 层壁垒 / N 种策略

Create a framework. Prefer two to five parts.

## 分别看每一层

Use concrete products, workflows, permissions, costs, incentives, or failure modes.

## 到这里，结论变清楚了

Tie the pieces together and remove weaker interpretations.

## 这意味着什么

Explain the impact for users, developers, platforms, or enterprises.

## 结论

Close with one or two strong paragraphs.
```

## Common Moves

- Convert vague debates into named dimensions: openness vs reliability, CLI vs MCP vs Skills, platform lock-in vs user agency, model ability vs harness quality.
- Use tables for comparisons. Keep columns judgment-oriented: "代表", "优势", "缺什么", "卡在哪里", "逻辑".
- Use Mermaid diagrams to compress relationships, flows, and bottlenecks. Diagrams must clarify the argument, not decorate it.
- Anchor abstractions with named products or concrete workflows: GitHub, Vercel, Feishu, Jira, Notion, Claude Code, OpenCode, Cursor, Dify, Alibaba, ByteDance, Tencent.
- Separate "can be built" from "can be used in a real organization".
- Distinguish technical feasibility, commercial incentive, organization approval, user experience, and regulation.

## Good Sentence Patterns

- "这不是 demo 能不能跑通的问题，而是默认前提在真实环境里是否成立。"
- "数据格式不统一是工程摩擦，不是架构壁垒。"
- "谁控制这一层，谁就控制 Agent 接触真实世界的方式。"
- "问题不在模型有没有能力，而在系统有没有给它可验证的反馈回路。"
- "CLI vs MCP 争的是管道，真正缺的是水龙头。"

## Evidence Standard

- Use sources for time-sensitive claims, product launches, benchmark numbers, pricing, legal/regulatory details, and market metrics.
- Prefer primary sources for official product behavior and technical architecture.
- If a claim is an inference from sources, phrase it as an inference.
- When citing benchmark or market numbers, qualify scope and avoid treating one dataset as universal.

## Final Checks

- Is the post making an ecosystem argument rather than merely listing products?
- Can the core claim be summarized in one memorable sentence?
- Did the article identify the real bottleneck instead of only describing symptoms?
- Are diagrams and tables doing analytical work?
- Are strong claims protected by concrete scope?
- Does the ending add judgment rather than restating the body?

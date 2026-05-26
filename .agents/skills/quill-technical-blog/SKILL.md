---
name: quill-technical-blog
version: 1.0.0
description: "Write and edit Quill technical engineering posts: implementation notes, debugging writeups, architecture explanations, tool usage, deployment, performance, reproducible workflows, and code-centered lessons. Use when the post should help readers understand or do a technical task."
---

# Quill Technical Blog

Use this skill for technical posts. The reader should leave with a clearer model of how something works and how to reproduce, debug, or adapt it.

Before finalizing, apply [`quill-author-voice`](../quill-author-voice/SKILL.md). Technical posts should read like engineering experience, not generic solution documentation.

## Positioning

This blog can publish technical writing, not only product or ecosystem analysis. In technical mode, the material is code, commands, configs, logs, APIs, runtime behavior, architecture, verification, and engineering tradeoffs.

The main promise is:

> 读者看完能更清楚地做成一件具体的技术事。

## Voice

- Write like a pragmatic programmer explaining a real engineering problem.
- Prefer precise mechanisms over broad industry takes.
- Be direct about failure modes and tradeoffs.
- Avoid tutorial fluff, marketing language, and "copy this blindly" recipes.
- Use Chinese by default for `content/zh/posts`; preserve the same structure when translating to English.

## Default Structure

Use this shape unless the topic requires a different one:

```markdown
## 我遇到的问题 / 想解决什么

State the concrete problem, target outcome, environment, and why the obvious route was not enough.

## 背景和约束

Name the runtime, framework, dependency, platform, auth model, data shape, version, or deployment constraints.

## 核心机制

Explain the underlying model. Use a Mermaid diagram when there are moving parts.

## 实现过程

Show important commands, config, code snippets, file layout, API calls, or patches.

## 踩坑和取舍

Explain weaker approaches, failure modes, edge cases, and why this design was chosen.

## 验证

Show how the result was checked: local command, tests, browser behavior, logs, benchmark, or before/after result.

## 结论

Extract the reusable engineering lesson.
```

## What To Include

- Minimal runnable examples where possible.
- Environment assumptions: OS, runtime, versions, hosting platform, API permission model, data shape.
- Exact commands when they are essential to reproduction.
- Short code snippets that expose the key mechanism.
- Logs or error messages when diagnosing a failure.
- File paths or config keys when location matters.
- Verification steps and expected observations.

## Common Moves

- Start from a concrete failure, not a generic introduction.
- Explain "why this works", not only "what to type".
- Include the failed or weaker approach if it teaches the boundary.
- When comparing designs, avoid false binaries. List the actual viable options considered and state why the chosen one fits the constraints.
- Separate local success from production/CI success.
- Distinguish implementation friction from architectural limitation.
- End with a pattern, checklist, or principle that can transfer to another project.

## Good Sentence Patterns

- "问题不在命令本身，而在它运行时拿到的上下文。"
- "这里真正需要固定的是输入边界，而不是输出格式。"
- "这个方案能跑，但一旦放到 CI 里会暴露两个问题。"
- "验证点不是页面能打开，而是状态能否跨 session 延续。"
- "这不是框架缺陷，而是我们没有把状态边界说清楚。"

## Evidence Standard

- Prefer local verification, official docs, source code, reproducible commands, and observed logs.
- Use current sources for recently changed APIs, SDK behavior, pricing, platform limits, or hosting behavior.
- When describing a benchmark, state the environment and scope.
- Do not turn one local observation into a universal claim.

## Final Checks

- Is the post actually technical, or did it drift into product commentary?
- Can the reader reproduce the important part, or understand why reproduction depends on local context?
- Are commands, code snippets, diagrams, or logs doing real explanatory work?
- Are assumptions and versions explicit enough?
- Does the conclusion name a reusable engineering lesson?

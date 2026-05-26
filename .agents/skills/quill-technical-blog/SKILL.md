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
## 问题复盘

State the incident, structural cause, impact, and chosen direction in one dense paragraph. Use a causal chain, not diary narration.

## 抽象边界

Name the interface, data boundary, runtime object, config key, storage/client boundary, or ownership boundary that made the implementation tractable.

## 方案取舍

List the real viable options considered. Explain what each option changes in failure mode, rollout risk, cost, consistency, or rollback.

## 实现

Show the smallest useful code, command, config, file layout, API call, or patch that exposes the mechanism.

## 接入改造

Explain the real work needed to migrate callers, remove old assumptions, or route existing entry points through the new boundary.

## 兼容细节 / 踩坑

Name the protocol, SDK, API, header, permission, or runtime behavior that differed from the happy path.

## 回退 / 验证

Show the operational knob, rollback path, local command, test, log, metric, benchmark, or before/after observation.

## 结论

Extract the narrow reusable lesson. Tie it back to the boundary chosen in the implementation.
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
- Put implementation before algorithm trivia when the implementation is the point. For example: explain the Router and threshold first, then explain why FNV-1a is enough.
- Separate local success from production/CI success.
- Distinguish implementation friction from architectural limitation.
- End with a pattern, checklist, or principle that can transfer to another project.

## Sentence Preference

- Use direct declarative sentences.
- Prefer "线上 R2 出现过短时网络问题，上传、转存、文件访问都受影响。" over broad setup.
- Prefer "按 id 哈希路由后，同一任务稳定落到同一个存储服务。" over "这不是随机分流，而是稳定路由。"
- Prefer "阈值为 95 时，95% 新上传走 R2，5% 走 OSS。" over abstract gray-release wording.
- Avoid repeating "核心是", "真正的问题是", "不是 A，而是 B", "不能只看 X，还要看 Y".

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

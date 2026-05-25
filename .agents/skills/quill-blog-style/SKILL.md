---
name: quill-blog-style
version: 1.0.0
description: "Write and edit articles for the Quill blog in its established style. Supports both technical engineering posts and AI Agent ecosystem/product analysis. Choose the mode from the post goal: implementation/repro/debugging for technical posts; market/platform/permission/incentive analysis for ecosystem posts."
---

# Quill Blog Style

Use this skill when writing, rewriting, outlining, reviewing, translating, or polishing posts for this repository's blog.

First choose the writing mode:

- **Technical engineering post**: use [`quill-technical-blog`](../quill-technical-blog/SKILL.md). The reader should understand, reproduce, debug, or implement something.
- **Ecosystem analysis post**: use [`quill-ecosystem-analysis`](../quill-ecosystem-analysis/SKILL.md). The reader should understand a structural shift, product category, platform incentive, or Agent industry bottleneck.

Do not force a technical post into a product/ecosystem essay. For technical posts, code, commands, system behavior, constraints, and verification are the main material.

## Voice

Write like a pragmatic systems-minded programmer.

- Prefer clear judgment over neutral summary.
- Be technically optimistic but not naive.
- Treat constraints as first-class: implementation details, runtime behavior, data access, permissions, reliability, platform incentives, organization approval, and engineering process.
- Avoid marketing language, hype, vague futurism, and emotional commentary.
- Use direct Chinese by default for `content/zh/posts`; keep English versions equally structured and unsentimental.

## Language Rules

- Prefer short paragraphs and high-density conclusion sentences.
- Keep headings concrete, not literary.
- Use bold for the main judgment in a section.
- Do not overuse rhetorical questions; one sharp question is enough.
- Avoid "可能有一定帮助", "值得关注一下", "未来可期" unless immediately made specific.
- Avoid empty balance. If there are tradeoffs, name the mechanism behind each side.

## Evidence Standard

- Use sources for time-sensitive claims, product launches, benchmark numbers, pricing, legal/regulatory details, and market metrics.
- For technical posts, prefer local verification, official documentation, source code, reproducible commands, and observed logs over secondary commentary.
- Do not present unverified current facts as stable truth.
- Prefer primary sources when discussing technical architecture or official product behavior.
- If a claim is an inference from sources, phrase it as an inference.
- Distinguish clearly between:
  - technical feasibility
  - commercial incentives
  - organization/security approval
  - user experience
  - regulatory pressure

## Style Checks Before Finalizing

- Did the chosen mode match the post goal: technical implementation vs ecosystem analysis?
- Can the article's core claim be summarized in one memorable sentence?
- Did the article identify the real bottleneck instead of only describing surface symptoms?
- Are diagrams, tables, code snippets, or command examples doing actual work?
- For technical posts, can a reader reproduce the important part or at least understand why reproduction depends on local context?
- Are strong claims protected by concrete scope?
- Does the ending add judgment rather than merely restating the body?
- Is the tone engineering-first, direct, and reality-bound?

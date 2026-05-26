---
name: quill-author-voice
version: 1.0.0
description: "Remove generic AI writing from Quill blog posts. Use when drafting, rewriting, or reviewing any post that should sound like the author: specific, experience-based, direct, and opinionated rather than neutral, padded, or template-like."
---

# Quill Author Voice

Use this skill after choosing the post type. It is a rewrite and review layer for making posts sound authored rather than generated.

## Core Rule

Specific beats generic every time.

Do not make the writing more "human" by adding jokes, slang, or fake casualness. Make it more human by adding concrete judgment, real constraints, failed paths, numbers when safe, and the author's bias.

For technical posts, default to direct declarative sentences. Avoid diary narration ("I first thought..."), repeated contrast formulas ("not A but B"), and padded transitions. State the fact, then the design consequence.

## Opening

Do not start with broad context.

Bad:

> 在现代后端系统中，对象存储的稳定性越来越重要。

Good:

> 一次任务会产出多类文件：音频、视频、封面图、中间图片。对象存储灰度如果按单次上传随机分流，比例没问题，但同一任务会在两个后端之间漂。

Open with one of:

- a concrete failure
- a wrong first assumption
- a direct judgment
- a specific engineering constraint

Avoid chronological diary openings unless the sequence itself matters. Prefer a technical judgment over "I first thought... later realized...".
Avoid overusing "不是 A，而是 B". It creates a punchy sentence but often breaks narrative flow. Prefer a cause-and-effect chain: constraint -> consequence -> design choice.

## Anti-AI Edits

Delete or rewrite:

- Generic setup: "随着技术发展", "在当今时代", "越来越重要"
- Empty balance: "既有优势，也有挑战"
- Safe summaries: "这对系统稳定性有重要意义"
- Overexplaining obvious code
- Template transitions: "首先", "其次", "此外", "总之", "值得注意的是", "不可忽视的是"
- Neutralized claims that avoid saying what the author actually thinks

Replace with concrete transitions:

- "问题出在这里：..."
- "这个约束会带来一个后果：..."
- "所以路由粒度要落在..."
- "这一步的作用是..."
- "这里不能按单次上传随机..."

## Paragraph Standard

Every paragraph should pass at least one test:

- It contains a concrete object, number, command, code path, error shape, or runtime behavior.
- It explains why a design choice was made.
- It names a tradeoff or rejected approach.
- It states a clear judgment that would be weaker if removed.

If a paragraph only says something generally positive, delete it.

## Technical Posts

For technical posts, prefer:

- first-person where it clarifies the origin of the decision
- the original wrong assumption
- the small detail that caused real work
- code snippets only where they expose the mechanism
- operational knobs and what they mean
- boundaries: where the design is enough, where it is not

Do not turn a technical post into a product case study. The reader should feel the engineering pressure, not read a sanitized achievement report.

## Rewrite Workflow

1. Write the blunt thesis in one sentence.
2. Add one concrete scene or constraint.
3. Keep only the code that explains the mechanism.
4. Replace generic nouns with actual system concepts.
5. Remove template transitions.
6. Add one "why not X" section when there was a real rejected approach.
7. End with a lesson that is narrower than a universal principle.

## Final Check

Before finalizing, list mentally:

- What did the author personally learn?
- What sentence would a generic AI article never write?
- What details were kept specific without exposing sensitive information?
- What correct but useless sentence was deleted?

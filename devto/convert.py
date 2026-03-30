#!/usr/bin/env python3
"""Convert Mermaid diagrams to mermaid.ink image URLs for Dev.to publication."""

import base64
import re
import os
import json

SOURCE_DIR = "/Users/zt-user/docs/quill/content/en/posts"
OUTPUT_DIR = "/Users/zt-user/docs/quill/devto"

HASHNODE_URLS = {
    "/posts/cli-vs-mcp-vs-skills/": "https://abin.hashnode.dev/cli-vs-mcp-vs-skills-the-whole-debate-is-asking-the-wrong-question",
    "/posts/agent-bottleneck-data-sovereignty/": "https://abin.hashnode.dev/your-agent-cant-help-you-and-its-not-because-its-dumb",
    "/posts/visual-vs-api-permission/": "https://abin.hashnode.dev/agents-behind-walls-who-will-push-over-the-first-brick",
}

ARTICLES = [
    {
        "source": "cli-vs-mcp-vs-skills.md",
        "output": "01-cli-vs-mcp-vs-skills.md",
        "devto_tags": ["ai", "mcp", "cli", "agents"],
        "canonical": HASHNODE_URLS["/posts/cli-vs-mcp-vs-skills/"],
    },
    {
        "source": "agent-bottleneck-data-sovereignty.md",
        "output": "02-agent-bottleneck-data-sovereignty.md",
        "devto_tags": ["ai", "agents", "data", "enterprise"],
        "canonical": HASHNODE_URLS["/posts/agent-bottleneck-data-sovereignty/"],
    },
    {
        "source": "visual-vs-api-permission.md",
        "output": "03-visual-vs-api-permission.md",
        "devto_tags": ["ai", "agents", "alibaba", "opensource"],
        "canonical": HASHNODE_URLS["/posts/visual-vs-api-permission/"],
    },
]


def mermaid_to_img_url(mermaid_code: str) -> str:
    """Convert Mermaid code to a mermaid.ink image URL."""
    encoded = base64.urlsafe_b64encode(mermaid_code.strip().encode("utf-8")).decode("utf-8").rstrip("=")
    return f"https://mermaid.ink/img/{encoded}"


def extract_alt_text(mermaid_code: str, index: int) -> str:
    """Extract a meaningful alt-text from the Mermaid diagram."""
    # Try subgraph title
    m = re.search(r'subgraph\s+"([^"]+)"', mermaid_code)
    if m:
        return m.group(1)
    # Try subgraph without quotes
    m = re.search(r'subgraph\s+(\S.*)', mermaid_code)
    if m:
        return m.group(1).strip()
    # Fall back
    return f"Diagram {index}"


def parse_frontmatter(content: str):
    """Parse Hugo YAML frontmatter, return (metadata_dict, body)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    # Manual parse (avoid yaml dependency issues)
    fm = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, parts[2].lstrip("\n")


def convert_footnotes(text: str) -> str:
    """Convert [^N] footnote syntax to plain [N] references."""
    # Convert inline refs [^N] (not followed by :) to [N]
    text = re.sub(r"\[\^(\d+)\](?!:)", r"[\1]", text)
    # Convert definition lines [^N]: to **[N]**:
    text = re.sub(r"^\[\^(\d+)\]:", r"**[\1]**:", text, flags=re.MULTILINE)
    return text


def fix_internal_links(text: str) -> str:
    """Replace Hugo internal links with Hashnode URLs."""
    for path, url in HASHNODE_URLS.items():
        text = text.replace(f"({path})", f"({url})")
    return text


def process_article(article: dict) -> dict:
    """Process one article: convert mermaid blocks, fix links, output Dev.to markdown."""
    source_path = os.path.join(SOURCE_DIR, article["source"])
    with open(source_path, "r") as f:
        content = f.read()

    fm, body = parse_frontmatter(content)
    title = fm.get("title", article["source"])

    # Replace mermaid code blocks with image URLs
    counter = [0]
    urls_generated = []

    def replace_mermaid(match):
        counter[0] += 1
        code = match.group(1)
        alt = extract_alt_text(code, counter[0])
        url = mermaid_to_img_url(code)
        urls_generated.append(url)
        return f"![{alt}]({url})"

    body = re.sub(r"```mermaid\n(.*?)```", replace_mermaid, body, flags=re.DOTALL)

    # Fix footnotes and internal links
    body = convert_footnotes(body)
    body = fix_internal_links(body)

    # Build Dev.to frontmatter
    tags = ", ".join(article["devto_tags"])
    devto_content = f"""---
title: "{title}"
published: false
tags: {tags}
series: "Thinking About the Agent Ecosystem"
canonical_url: "{article['canonical']}"
---

{body}"""

    output_path = os.path.join(OUTPUT_DIR, article["output"])
    with open(output_path, "w") as f:
        f.write(devto_content)

    print(f"  {article['output']}: {counter[0]} diagrams converted")
    return {
        "path": output_path,
        "title": title,
        "diagrams": counter[0],
        "first_url": urls_generated[0] if urls_generated else None,
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Converting articles for Dev.to...")
    results = []
    for article in ARTICLES:
        result = process_article(article)
        results.append(result)

    total = sum(r["diagrams"] for r in results)
    print(f"\nDone. {total} diagrams converted across {len(results)} articles.")
    print(f"\nTest URL (first diagram of article 01):")
    print(f"  {results[0]['first_url']}")


if __name__ == "__main__":
    main()

---
title: "Your Agent Can't Help You — And It's Not Because It's Dumb"
date: 2026-03-26T14:00:00+08:00
draft: false
series: ["Thinking About the Agent Ecosystem"]
tags: ["AI Agent", "Data Barriers", "Permissions", "Enterprise IT"]
summary: "The LLM is capable enough. The CLI is efficient enough. MCP is standardized enough. But try asking your agent to write your weekly status report — it can't even read your Slack messages. The problem comes down to two distinct walls."
mermaid: true
---

> [In the previous post](/posts/cli-vs-mcp-vs-skills/) we argued that the CLI vs. MCP debate is really a debate about pipes — and what's actually missing is the faucet. This post digs one level deeper: even if you open the faucet, you probably still can't connect to it. The reasons agents struggle in the real world are more structural than most people realize.

## A Common Promise

"Let an agent automatically write your weekly status report — it reads your Git commits, Slack channel history, Jira ticket updates, and Google Calendar meetings, then generates a report your manager can actually read."

This is the story agent products love to tell. It sounds reasonable — the data is all yours, you're already using all the tools, you're just automating what you'd otherwise do by hand.

But if you actually try it, you'll find that only 1 out of 5 data sources works:

![diagram](https://mermaid.ink/img/Z3JhcGggVEIKICAgIEFnZW50WyJBZ2VudDogV3JpdGUgeW91ciB3ZWVrbHkgcmVwb3J0Il0KICAgIAogICAgQWdlbnQgLS0-IEdpdFsiR2l0IGxvZyDinIU8YnIvPlNTSCBrZXkgaXMgbG9jYWwsIHdvcmtzIGltbWVkaWF0ZWx5Il0KICAgIEFnZW50IC0tPiBTbGFja1siU2xhY2sgbWVzc2FnZXMg4p2MPGJyLz5SZXF1aXJlcyBjcmVhdGluZyBhIFNsYWNrIGFwcCBhbmQgYWRtaW4gYXBwcm92YWwiXQogICAgQWdlbnQgLS0-IEppcmFfdFsiSmlyYSB0aWNrZXRzIOKdjDxici8-SVQgaGFzIGRpc2FibGVkIFBlcnNvbmFsIEFjY2VzcyBUb2tlbnMiXQogICAgQWdlbnQgLS0-IENhbFsiR29vZ2xlIENhbGVuZGFyIOKdjDxici8-T0F1dGggYXBwIHJlcXVpcmVzIGFkbWluIHdoaXRlbGlzdCJdCiAgICBBZ2VudCAtLT4gRW1haWxbIkVtYWlsIOKdjDxici8-Q29ycG9yYXRlIElNQVAgaXMgYmxvY2tlZCBieSBzZWN1cml0eSBwb2xpY3kiXQogICAgCiAgICBHaXQgLS0-IE9LWyLinIUgQWNjZXNzaWJsZSJdCiAgICBTbGFjayAtLT4gQmxvY2tlZFsi4p2MIEluYWNjZXNzaWJsZSJdCiAgICBKaXJhX3QgLS0-IEJsb2NrZWQKICAgIENhbCAtLT4gQmxvY2tlZAogICAgRW1haWwgLS0-IEJsb2NrZWQKICAgIAogICAgc3R5bGUgQWdlbnQgZmlsbDojNjM2NmYxLGNvbG9yOiNmZmYKICAgIHN0eWxlIE9LIGZpbGw6IzIyYzU1ZSxjb2xvcjojZmZmCiAgICBzdHlsZSBCbG9ja2VkIGZpbGw6I2VmNDQ0NCxjb2xvcjojZmZm?)

It's not that the agent isn't smart enough. It's not that the CLI isn't efficient enough. **The data simply isn't reachable.**

There are, of course, some "workaround" approaches that try to bypass this limitation: browser extensions that piggyback on your login session to scrape Slack messages, RPA tools that simulate clicks to export Jira data, reverse-engineered wrappers around corporate email APIs. These can make a demo work. But they're fundamentally web scrapers — a UI redesign breaks them, a security policy update kills them, and the legal exposure never goes away. Building a workflow on top of these approaches is building on quicksand.

We'll take a detailed look at these "workaround" approaches and their limitations in [the third post](/posts/visual-vs-api-permission/). For now, let's focus on a more fundamental question: **why don't the legitimate paths work?**

## An Agent's Real Capability Depends on Three Variables

![diagram](https://mermaid.ink/img/Z3JhcGggTFIKICAgIHN1YmdyYXBoICJBZ2VudCBjYXBhYmlsaXR5ID0gdGhlIGludGVyc2VjdGlvbiBvZiBhbGwgdGhyZWUiCiAgICAgICAgQVsiTExNIHJlYXNvbmluZyBhYmlsaXR5PGJyLz7inIUgQWxyZWFkeSBzdWZmaWNpZW50IGluIDIwMjYiXQogICAgICAgIEJbIlRvb2wtY2FsbGluZyBlZmZpY2llbmN5PGJyLz7inIUgQ0xJIGFuZCBTa2lsbHMgbGFyZ2VseSBzb2x2ZWQiXQogICAgICAgIENbIkFjY2Vzc2libGUgZGF0YSBzY29wZTxici8-4p2MIFNldmVyZWx5IGxhY2tpbmciXQogICAgZW5kCiAgICAKICAgIHN0eWxlIEEgZmlsbDojMjJjNTVlLGNvbG9yOiNmZmYKICAgIHN0eWxlIEIgZmlsbDojMjJjNTVlLGNvbG9yOiNmZmYKICAgIHN0eWxlIEMgZmlsbDojZWY0NDQ0LGNvbG9yOiNmZmY=?)

The entire industry is racing to improve LLM capability and tool protocols. But the real bottleneck is data access. It's like having a top-of-the-line race car and a perfect track — with an empty fuel tank.

## Two Walls: Why the Data Is Out of Reach

"Data is inaccessible" isn't a vague problem. It has two distinct walls, each with a fundamentally different character:

![diagram](https://mermaid.ink/img/Z3JhcGggVEIKICAgIHN1YmdyYXBoICJXYWxsIDE6IFBsYXRmb3JtIExvY2tkb3duIgogICAgICAgIFcxWyJXaGF0c0FwcCwgQW1hem9uLCBEb29yRGFzaCwgVGlrVG9rPGJyLz5ObyBvcGVuIEFQSTxici8-VGhlaXIgYnVzaW5lc3MgbW9kZWwgZGVwZW5kcyBvbiBrZWVwaW5nIGl0IGNsb3NlZCJdCiAgICBlbmQKICAgIAogICAgc3ViZ3JhcGggIldhbGwgMjogT3JnYW5pemF0aW9uYWwgQ29udHJvbCIKICAgICAgICBXMlsiU2xhY2ssIEppcmEsIEdvb2dsZSBXb3Jrc3BhY2U8YnIvPlBsYXRmb3JtIGhhcyBhbiBBUEksIGJ1dCBjb3Jwb3JhdGUgSVQgd29uJ3QgYXBwcm92ZSBpdDxici8-WW91IGNhbiBzZWUgdGhlIGRhdGEsIGJ1dCB5b3VyIHByb2dyYW0gY2FuJ3QgcmVhZCBpdCJdCiAgICBlbmQKICAgIAogICAgVzEgLS0-IFcyCiAgICAKICAgIFcyIC0tPiBBZnRlclsiT25jZSB5b3UgaGF2ZSB0aGUgZGF0YTxici8-SW5jb25zaXN0ZW50IGZvcm1hdHM_IExMTSBjYW4gaGFuZGxlIHRoYXQ8YnIvPuKGkSBUaGF0J3MgZW5naW5lZXJpbmcgZnJpY3Rpb24sIG5vdCBhIHdhbGwiXQogICAgCiAgICBzdHlsZSBXMSBmaWxsOiNlZjQ0NDQsY29sb3I6I2ZmZgogICAgc3R5bGUgVzIgZmlsbDojZjk3MzE2LGNvbG9yOiNmZmYKICAgIHN0eWxlIEFmdGVyIGZpbGw6IzIyYzU1ZTIwLHN0cm9rZTojMjJjNTVl?)

Wall 1 gets the most attention, but in practice, **Wall 2 is the one most people actually hit.**

### Wall 1: Platform Lockdown

WhatsApp won't ship a CLI. Amazon won't open a price-comparison API. TikTok won't give you access to its recommendation data. [The previous post](/posts/cli-vs-mcp-vs-skills/) argued from a technical standpoint that CLI is perfectly capable of implementing OAuth (`gh auth login` is proof), so this isn't a technical barrier[^1].

**So why don't they do it? Because data enclosure is the foundation of these platforms' business models.**

Once an agent can make optimal decisions on a user's behalf — comparing prices, comparing ratings, searching across platforms — the platform loses its ability to steer user behavior through recommendation algorithms. That directly threatens the core revenue from advertising and traffic monetization.

A simple heuristic: **whether a platform will open up to agents depends entirely on whether opening up serves its commercial interests.**

| Platform type | Examples | Open to agents? | Logic |
|--------------|---------|----------------|-------|
| Sells subscriptions / services | GitHub, Notion, Vercel | ✅ Actively open | More agent integrations → users more dependent → more paid conversions |
| Sells traffic / advertising | WhatsApp, Amazon, TikTok | ❌ Locked down | Agents help users skip recommendations → ad value drops |
| Sells enterprise software | Slack, Microsoft Teams | ⚠️ Partially open | Rich bot ecosystem → enterprises more dependent on the platform |

### Wall 2: Organizational Control — Visible Doesn't Mean Accessible

Here's a concrete example. You open Slack in your browser at work and can see all your channel history and shared files. Now you want to write a script so an agent can read the same messages. You'll discover you need to create a Slack App on the Slack API dashboard, request `channels:history` and `channels:read` scopes, and then submit it to your workspace admin for approval. The admin might ask what you need the permission for — and then deny you.

**Data you can see in a browser is not necessarily data your program can read.** The two paths use completely different authentication chains:

![diagram](https://mermaid.ink/img/Z3JhcGggVEIKICAgIEwxWyJWaXN1YWwgYWNjZXNzPGJyLz5DYW4gc2VlIGl0IGluIGEgYnJvd3NlciJdIC0tPnwi4pyFIFlvdSBoYXZlIHRoaXMifCBPSzFbIlVzaW5nIGl0IGV2ZXJ5IGRheSJdCiAgICBMMlsiQVBJIGFjY2Vzczxici8-Q2FuIGV4dHJhY3QgaXQgdmlhIHByb2dyYW1tYXRpYyBpbnRlcmZhY2UiXSAtLT58IuKdkyBOb3QgZ3VhcmFudGVlZCJ8IE1heWJlWyJSZXF1aXJlcyBhbiBBUEkgdG9rZW4iXQogICAgTDNbIk9yZ2FuaXphdGlvbmFsIGF1dGhvcml6YXRpb248YnIvPkNvcnBvcmF0ZSBJVCBhbGxvd3MgeW91IHRvIGNhbGwgdGhlIEFQSSJdIC0tPnwi4p2MIFByb2JhYmx5IG5vdCJ8IE5vcGVbIlNlY3VyaXR5IHBvbGljeSBibG9ja3MgaXQiXQogICAgCiAgICBzdHlsZSBMMSBmaWxsOiMyMmM1NWUsY29sb3I6I2ZmZgogICAgc3R5bGUgTDIgZmlsbDojZWFiMzA4LGNvbG9yOiNmZmYKICAgIHN0eWxlIEwzIGZpbGw6I2VmNDQ0NCxjb2xvcjojZmZm?)

Every day you open Slack to read messages, check Jira tickets, and read email — that's **visual access**. Your browser holds the session, cookies are sent automatically, everything is seamless.

But an agent takes a completely different authentication path:

![diagram](https://mermaid.ink/img/Z3JhcGggVEIKICAgIHN1YmdyYXBoICJCcm93c2VyIGFjY2VzcyIKICAgICAgICBCcm93c2VyWyJZb3VyIGJyb3dzZXIiXQogICAgICAgIEJyb3dzZXIgLS0-IENvb2tpZVsiQ29va2llIC8gU2Vzc2lvbjxici8-U2VudCBhdXRvbWF0aWNhbGx5Il0KICAgICAgICBDb29raWUgLS0-IFNlcnZlclsiU2VydmVyIHJldHVybnMgZGF0YSJdCiAgICBlbmQKICAgIAogICAgc3ViZ3JhcGggIkFnZW50IC8gQVBJIGFjY2VzcyIKICAgICAgICBBZ2VudEFQSVsiQWdlbnQgLyBzY3JpcHQiXQogICAgICAgIEFnZW50QVBJIC0tPnwicmVxdWlyZXMifCBUb2tlblsiQVBJIFRva2VuIC8gT0F1dGggQ3JlZGVudGlhbCJdCiAgICAgICAgVG9rZW4gLS0-fCJyZXF1aXJlcyJ8IElUWyJJVCBkZXBhcnRtZW50IGFwcHJvdmFsIl0KICAgICAgICBJVCAtLT58InJlcXVpcmVzInwgUG9saWN5WyJTZWN1cml0eSBwb2xpY3kgYWxsb3dzIGl0Il0KICAgICAgICBQb2xpY3kgLS0-IEFQSVsiQVBJIHNlcnZlciJdCiAgICBlbmQKICAgIAogICAgQnJvd3NlciAtLi0-fCJUd28gY29tcGxldGVseSBkaWZmZXJlbnQgcGF0aHMifCBBZ2VudEFQSQogICAgCiAgICBzdHlsZSBCcm93c2VyIGZpbGw6IzIyYzU1ZSxjb2xvcjojZmZmCiAgICBzdHlsZSBBZ2VudEFQSSBmaWxsOiNlZjQ0NDQsY29sb3I6I2ZmZgogICAgc3R5bGUgSVQgZmlsbDojZjk3MzE2LGNvbG9yOiNmZmY=?)

**Having the former doesn't mean you have the latter. Agents can only take the latter path.**

From the perspective of an ordinary developer (non-admin), here's the actual API accessibility of common tools:

| Tool | Visible in browser | Callable via API | Where it gets stuck |
|------|-------------------|-----------------|-------------------|
| **Git (local)** | ✅ | ✅ | SSH key is local — no approval needed |
| **Slack** | ✅ | ❌ | Creating a Slack App requires workspace admin approval for sensitive scopes[^2] |
| **Microsoft Teams** | ✅ | ❌ | Custom apps require IT admin sideloading approval |
| **Jira Cloud** | ✅ | ⚠️ | Depends on whether the company has disabled Personal Access Tokens |
| **Corporate email** | ✅ | ❌ | IMAP/SMTP typically blocked by security policy |
| **Google Workspace** | ✅ | ❌ | OAuth apps require admin to whitelist them |
| **Notion (personal)** | ✅ | ✅ | Personal Integrations don't require workspace admin involvement[^3] |

The conclusion is clear: **the only things you can freely access via API are local files, personal Git repositories, and personal Notion workspaces.** Everything else is blocked at the organizational admin approval step.

This also explains a pattern: why is coding assistance currently the most successful agent use case? Because code lives in your local filesystem — no one's permission required.

### A Note: What Happens After You Get the Data?

Someone might ask: even if you break through both walls, the data is scattered across Git, Slack, Jira, email, and other systems in different formats — doesn't that count as a third wall?

Honestly, **with 2026-era LLMs, this isn't a real barrier.** Git log is plain text, Jira's API returns JSON, Slack messages are structured data — as long as data can be converted to text, current models can read and synthesize it. Identity mapping (Git email ≠ Slack user_id) just needs to be told to the model once. Time alignment, semantic extraction, deduplication and categorization — these are exactly what LLMs are best at.

Inconsistent data formats are engineering friction, not an architectural barrier. They're not in the same league as the first two walls (platform lockdown and organizational denial of access).

**The only two things that actually block agents are: platforms that won't open up, and organizations that won't allow it.** Once the data is in hand, the model can handle the rest.

## The Real Boundaries of Agent Capability

Taking both walls into account, here are the true capability boundaries for agents in 2026:

| Use case | Technically feasible | Actually usable | Blocked by |
|---------|---------------------|----------------|-----------|
| Coding assistance (writing code, debugging) | ✅ | ✅ | No wall — code is local |
| Search public information and summarize | ✅ | ✅ | No wall — public internet data |
| Auto-write weekly status report | ✅ | ❌ | Wall 2: Slack / Jira API permissions |
| Cross-platform price comparison (flights, hotels) | ✅ | ❌ | Wall 1: Booking.com / airline sites not open |
| Customer relationship management | ✅ | ❌ | Wall 2: CRM API requires IT approval |
| Auto-process email | ✅ | ❌ | Wall 2: IMAP is blocked |
| Cross-platform content publishing | ✅ | ❌ | Wall 1: platforms don't interoperate |
| Personal health data analysis | ✅ | ❌ | Wall 1: health apps don't open up |

**Technically feasible across the board. Actually doable for almost none of them.**

## Conclusion

Your agent can't help you — not because it isn't smart enough. It's because of two walls:

1. **Platform lockdown**: Business models are built on data enclosures. They won't voluntarily open their APIs. This is a commercial negotiation problem.
2. **Organizational control**: Even when a platform has an API, your company's IT security policy may not allow you to use it. This is an organizational management problem.

As for inconsistent data formats and the need to integrate information across systems — with current LLM capability, that's just engineering friction, not a real obstacle. **Once the data is in hand, the model can handle it. The problem is that the data never gets there.**

And most agent product marketing never mentions any of this. It simply assumes "you have API access."

Next time someone pitches you on "automating your workflow with agents," ask two questions first:

> 1. Does the platform provide an API for this data?
> 2. Does my organization allow individuals to use that API?

Both need to be Yes for anything to actually work. In the reality of 2026, scenarios where both are Yes are still rare.

---

*This is the second post in the "Thinking About the Agent Ecosystem" series. Next up: since the data is out of reach, who is working around it and how? Alibaba's closed-loop ecosystem, Doubao's screen-scraping phone agent, and what forces might eventually push things toward openness.*

---

## References

[^1]: On the relationship between platform data lockdown and business models, see [MCP vs. CLI for AI Agents: The Answer Is Both](https://aiproductivity.ai/news/mcp-vs-cli-ai-agents-comparison/) and [The MCP vs CLI Debate Is Missing the Point](https://mkweb.dev/blog/mcp-vs-cli-missing-the-point). The [first post in this series](/posts/cli-vs-mcp-vs-skills/) argued from a technical standpoint that CLI is fully capable of implementing OAuth — so the reason platforms don't open up is a business choice, not a technical limitation.

[^2]: Creating a Slack App with sensitive OAuth scopes (such as `channels:history`, `chat:write`) requires workspace admin approval. See the [Slack API documentation on scopes](https://api.slack.com/scopes). Enterprise Grid workspaces enforce even stricter approval workflows for custom integrations.

[^3]: Notion's Internal Integration allows individual users to create integrations directly, without involving a workspace administrator; see the [Notion API documentation](https://developers.notion.com/docs/create-a-notion-integration). This makes it one of the few collaboration tools that supports personal-level OAuth.

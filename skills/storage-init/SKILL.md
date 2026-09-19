---
name: storage-init
description: Initialize or review global storage preferences and per-project routing. Use when the user asks to set up storage, choose storage engines, run storage-init, change storage tiers, or configure where tasks, notes, and artifacts are saved. Discovers current session capabilities; no provider or MCP server is required.
license: MIT
---

# Storage Init

Load the [Adaptive Storage skill](../adaptive-storage/SKILL.md) and its [first-use setup](../adaptive-storage/references/setup.md) reference through the host's skill/resource loader when available. These relative links describe the bundled sibling layout for filesystem hosts; they do not require filesystem access. Both skills and their references are distributed together. Treat installation as incomplete only when neither the host loader nor the bundled resources can provide the matching skill and setup reference; help restore access rather than inventing a reduced setup policy.

Run the same capability discovery and configuration workflow used by automatic first activation. Resolve saved configuration first. With an existing policy, show its effective routes and ask only what the user wants to change; do not reset configuration or migrate records merely because initialization was invoked again.

Without a completed policy, discover available engines, explain suitable arrangements and their tradeoffs, and obtain the user's selection. Configure global defaults for new projects or a project-specific override according to the user's requested scope. Keep tasks, notes, and artifact routes separate and record unresolved types honestly.

The host may expose this skill as `/storage-init`, `$storage-init`, `/skill:storage-init`, a namespaced plugin command, or a natural-language invocation. Use the host's actual interface; a Markdown file does not register a universal slash command.

After setup, verify the saved policy, summarize working/durable/shared destinations and publication timing, and report its non-secret locator. If cross-session persistence is unavailable, say so. Installation, initialization, and backend migration are separate actions. Do not install services or copy historical records unless authorized.

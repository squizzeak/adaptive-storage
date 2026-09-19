# Platform Sources and Compatibility Notes

This page records the primary vendor documentation used for Adaptive Storage's installation guidance. It was checked on **2026-09-19**. Agent hosts evolve quickly; use the linked vendor page when a current client disagrees with this repository.

## Compatibility matrix

| Host | Direct user skill paths | Native install or distribution route used here | Global instruction file | Verified caveat |
| --- | --- | --- | --- | --- |
| Codex | `~/.agents/skills/<name>/SKILL.md` | Codex marketplace at `.agents/plugins/marketplace.json`; register with `codex plugin marketplace add` | `~/.codex/AGENTS.md` | Adding a marketplace registers a source. Codex CLI 0.155.0 also exposes `codex plugin add`; current OpenAI web docs direct local plugin installation and testing through the ChatGPT desktop app. |
| GitHub Copilot CLI | `~/.copilot/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | Copilot CLI marketplace; it recognizes `.claude-plugin/marketplace.json` | `~/.copilot/copilot-instructions.md` | `copilot skill add` and `copilot plugin install` are separate systems. A marketplace plugin install uses `plugin@marketplace`. |
| Claude Code | `~/.claude/skills/<name>/SKILL.md` | Claude Code marketplace at `.claude-plugin/marketplace.json` | `~/.claude/CLAUDE.md` | Personal filesystem skills are local-machine skills. Claude cloud and Cowork sessions have separate skill availability rules. |
| OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | Direct discovery, or Vercel's community `skills` CLI targeting OpenCode | `~/.config/opencode/AGENTS.md` | No OpenCode-native marketplace or Codex/Claude marketplace compatibility is claimed. OpenCode's plugin system is distinct from Agent Skills discovery. |
| Pi | `~/.pi/agent/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | Direct discovery or `pi install` from a Git package with a conventional `skills/` directory | `~/.pi/agent/AGENTS.md` | Pi says models do not always load a matching skill; `/skill:<name>` forces it. Pi packages are a Pi package mechanism, not a universal marketplace. |
| Gemini CLI | `~/.gemini/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` | Direct discovery or Gemini's native `gemini skills` utilities | `~/.gemini/GEMINI.md` | Gemini requires activation consent each time a skill triggers. Extensions and Agent Skills are separate systems. |

## Codex and ChatGPT

Primary sources:

- [Build skills — OpenAI](https://developers.openai.com/codex/skills/)
- [Package your plugin — OpenAI](https://developers.openai.com/plugins/build/plugins)
- [Plugin submission errors — OpenAI](https://developers.openai.com/plugins/deploy/submission-errors)
- [Custom instructions with AGENTS.md — OpenAI](https://developers.openai.com/codex/guides/agents-md)

Facts used:

- Current Codex scans `.agents/skills` from the working directory to the repository root and uses `$HOME/.agents/skills` for user skills.
- Skills are progressively disclosed. Codex initially sees names and descriptions and loads a complete `SKILL.md` after selection. Explicit `$skill-name` invocation is supported.
- Plugins can contain one or more skills and may, but do not have to, contain MCP connections.
- Repository marketplaces use `.agents/plugins/marketplace.json`; personal marketplaces use `~/.agents/plugins/marketplace.json`.
- `codex plugin marketplace add` registers a Git or local marketplace source. OpenAI's current page says to use the ChatGPT desktop app to install and test a local plugin.
- A skill inside a plugin has the combined identity `plugin-name:skill-name`. Skill-picker rendering and command completion can vary by client, so this repository directs users to select the combined identity instead of promising that typed syntax works in every client.
- Codex reads global instructions from `AGENTS.override.md` or `AGENTS.md` in `CODEX_HOME`, which defaults to `~/.codex`.

Compatibility note: older material and some existing installations use `~/.codex/skills`. The current OpenAI skill-location table names `~/.agents/skills` for user scope, so this repository documents the current path and does not rely on the older one. A local read of `codex plugin add --help` in Codex CLI 0.155.0 on 2026-09-19 confirmed `codex plugin add NAME@MARKETPLACE`; that executable evidence supplements the web documentation and is version-qualified rather than presented as universal behavior.

## GitHub Copilot CLI

Primary sources:

- [Adding agent skills for GitHub Copilot CLI — GitHub](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [GitHub Copilot CLI configuration directory — GitHub](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [GitHub Copilot CLI plugin reference — GitHub](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Adding custom instructions for GitHub Copilot CLI — GitHub](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)

Facts used:

- Personal Agent Skills are supported at `~/.copilot/skills` and `~/.agents/skills`.
- `copilot skill add` manages skills. Installing a directory registers it as a skill source; installing a file or URL copies skill content.
- Copilot CLI supports plugins from a registered marketplace, GitHub repository, Git URL, or local path.
- Copilot marketplace catalogs normally use `.github/plugin/marketplace.json`, and the CLI also checks `.claude-plugin/marketplace.json`.
- `copilot plugin marketplace add OWNER/REPO` registers a catalog; `copilot plugin install plugin@marketplace` installs one entry.
- Copilot's slash command reference qualifies a plugin skill as `/plugin-name/skill-name`; direct skills use `/skill-name`.
- `~/.copilot/copilot-instructions.md` applies across repositories. `COPILOT_HOME` replaces the `~/.copilot` root when set.

Compatibility note: a raw `SKILL.md` URL is insufficient when a skill depends on sibling references or assets. Adaptive Storage therefore documents a complete-folder copy or the plugin bundle.

## Claude Code

Primary sources:

- [Extend Claude with skills — Anthropic](https://code.claude.com/docs/en/skills)
- [Discover and install plugins through marketplaces — Anthropic](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a plugin marketplace — Anthropic](https://code.claude.com/docs/en/plugin-marketplaces)
- [How Claude remembers your project — Anthropic](https://code.claude.com/docs/en/memory)

Facts used:

- Personal skills live at `~/.claude/skills/<skill-name>/SKILL.md` and are available to local projects on that machine.
- Claude can choose a skill from its description or the user can invoke it directly as `/skill-name`.
- Plugin skills are namespaced as `/plugin-name:skill-name`.
- A GitHub marketplace is added with `claude plugin marketplace add owner/repo`; a plugin is installed with `claude plugin install plugin@marketplace`.
- The marketplace manifest is `.claude-plugin/marketplace.json`.
- User instructions live at `~/.claude/CLAUDE.md`.

Compatibility note: local `~/.claude/skills` do not automatically appear in Claude cloud or Cowork sessions. Those surfaces use account-enabled skills, committed project skills where supported, or appropriately declared plugins.

## OpenCode

Primary sources:

- [Agent Skills — OpenCode](https://opencode.ai/docs/skills)
- [Instructions — OpenCode](https://opencode.ai/v2/docs/instructions)
- [Configuration — OpenCode](https://opencode.ai/docs/config/)
- [Skills CLI reference — skills.sh](https://skills.sh/docs/cli)
- [Skills CLI source and full command reference — Vercel Labs](https://github.com/vercel-labs/skills)
- [Introducing skills, the open agent skills ecosystem — Vercel](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)

Facts used:

- OpenCode natively discovers global skills from `~/.config/opencode/skills`, `~/.claude/skills`, and `~/.agents/skills`.
- Skills are loaded on demand with OpenCode's native `skill` tool.
- The global instruction file is `~/.config/opencode/AGENTS.md`.
- OpenCode plugins are configured separately through its configuration and npm-oriented plugin mechanism.
- Vercel's open source `skills` CLI accepts GitHub repositories, supports global installation, can select multiple named skills, and lists OpenCode as a target agent. The CLI's own documentation says anonymous telemetry is enabled by default and documents `DISABLE_TELEMETRY=1` as the opt-out.

Compatibility note: no primary OpenCode source found support for installing a Codex `.agents/plugins/marketplace.json` or Claude `.claude-plugin/marketplace.json`. skills.sh is a community directory and package installer, not an OpenCode-native marketplace. This repository therefore makes no native marketplace-compatibility claim for OpenCode.

## Pi

Primary sources:

- [Skills — Pi source documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
- [Pi Packages — Pi source documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)

Facts used:

- Pi discovers global skills from `~/.pi/agent/skills/` and `~/.agents/skills/`.
- Pi loads matching skills on demand and registers `/skill:<name>` commands. Its documentation explicitly warns that models do not always load a skill, so the command can force it.
- Pi packages may use a conventional top-level `skills/` directory and can be installed from a Git URL with `pi install`.
- Pi's global context file is `~/.pi/agent/AGENTS.md`.

Compatibility note: the Pi repository moved from `badlogic/pi-mono` to `earendil-works/pi`; the older URL redirects to the current first-party repository. The source documentation, rather than a community catalog, is the basis for the paths above.

## Gemini CLI

Primary sources:

- [Managing Agent Skills — Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/)
- [Provide context with GEMINI.md files — Gemini CLI](https://geminicli.com/docs/cli/gemini-md/)

Facts used:

- User skills live at `~/.gemini/skills/`, with `~/.agents/skills/` as a supported alias.
- `/skills list` shows discovered skills and `/skills reload` rescans them.
- `gemini skills install` and `gemini skills link` are native skill-management commands.
- Gemini asks for installation consent for a remote source and activation consent each time a skill triggers.
- The global context file is `~/.gemini/GEMINI.md`.

Compatibility note: Gemini Extensions can bundle skills, but an Extension is a separate package format. Adaptive Storage is distributed as a plain Agent Skill and does not claim to be a Gemini Extension.

## What “verified” means here

The matrix verifies that the host's current primary documentation names the path or command and that this repository's package layout targets that documented shape. It does not claim that every host version, managed organization policy, cloud execution surface, or model will load and invoke the skills identically.

Global discovery and session invocation are separate checks:

1. **Installed:** both complete skill folders exist in a documented location or an installed plugin.
2. **Discovered:** the host lists `storage-init` and `adaptive-storage` among available skills or exposes both through the plugin.
3. **Invoked:** the host loads `storage-init` for explicit setup or `adaptive-storage` for a matching persistent-work request.
4. **Initialized:** `storage-init`, or `adaptive-storage` on an unconfigured first use, records the global and/or project scope the user actually accepted. Project-only acceptance does not imply global initialization.
5. **Operational:** later task, note, and artifact requests read and update the selected local or remote destinations with the expected semantics.

The installation guide does not collapse these states into a single “works everywhere” claim.

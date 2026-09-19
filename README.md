# Adaptive Storage

Portable Agent Skills that discover the storage capabilities available in an agent session, let you choose global defaults and project overrides, and route tasks, notes, and artifacts through working, durable, shared, and archive roles.

Adaptive Storage is a workflow, not a hosted storage service. It ships no daemon, account, API, telemetry client, mandatory MCP server, or mandatory runtime. Your agent uses the files, Git tools, native records, connectors, APIs, or other storage capabilities that are actually available and authorized in its current host.

## Contents

- [What is included](#what-is-included)
- [Quick install](#quick-install)
- [Global first run](#global-first-run)
- [How storage is organized](#how-storage-is-organized)
- [How project work flows](#how-project-work-flows)
- [Examples](#examples)
- [Limitations](#limitations)
- [Verification status](#verification-status)
- [Documentation](#documentation)
- [Privacy and license](#privacy-and-license)

## What is included

The package contains two canonical skills. Install them together:

| Skill | Purpose |
| --- | --- |
| [`storage-init`](skills/storage-init/SKILL.md) | Explicitly initialize or review global preferences and per-project routing. |
| [`adaptive-storage`](skills/adaptive-storage/SKILL.md) | Run session preflight, discover capabilities, route persistent work, refresh relevant context, and publish with verification. If configuration is missing, it runs the same first-use setup automatically. |

Both skills read the same policy. `storage-init` is a convenient setup entry point, not a separate program or service.

The canonical skill folders live under `skills/`. The generated `plugins/adaptive-storage/skills/` copies support native plugin installation without adding runtime tools.

## Quick install

The repository is public at [`squizzeak/adaptive-storage`](https://github.com/squizzeak/adaptive-storage).

### Codex marketplace

```sh
codex plugin marketplace add squizzeak/adaptive-storage
codex plugin add adaptive-storage@adaptive-storage
```

The second command is exposed by Codex CLI 0.155.0. With a client that does not offer `codex plugin add`, restart the ChatGPT desktop app, open the Plugins Directory, select the **Adaptive Storage** source, and install the plugin there. Current OpenAI web documentation uses the CLI command to register the marketplace and the desktop app to install and test its local plugins.

### Claude Code marketplace

```sh
claude plugin marketplace add squizzeak/adaptive-storage
claude plugin install adaptive-storage@adaptive-storage
```

Then run `/adaptive-storage:storage-init` in Claude Code.

### GitHub Copilot CLI marketplace

```sh
copilot plugin marketplace add squizzeak/adaptive-storage
copilot plugin install adaptive-storage@adaptive-storage
```

Then ask Copilot to use `/adaptive-storage/storage-init`. Copilot's plugin-qualified skill separator is `/`, while Claude Code and OpenAI plugin identities use `:`.

### OpenCode native plugin or community Skills CLI

The optional [native OpenCode adapter](adapters/opencode/README.md) registers `/storage-init`, discovers both bundled skills, and adds storage-routing reminders to session model calls. Clone this repository and merge its absolute entrypoint into your global OpenCode configuration:

```json
{"plugin": ["file:///absolute/path/adaptive-storage/adapters/opencode/index.mjs"]}
```

Keep the complete checkout together, preserve existing configuration, and restart OpenCode. The adapter has no dependencies or mandatory MCP server. Its [installation guide](adapters/opencode/README.md) covers options, project scope, and verification.

For a skill-only installation, Vercel's open source `skills` CLI can install both skills into OpenCode's global skill directory:

```sh
npx skills add squizzeak/adaptive-storage -g -a opencode --skill adaptive-storage --skill storage-init
```

This is a community package installer backed by the skills.sh ecosystem. It is not an OpenCode-native marketplace or a claim that OpenCode understands either marketplace manifest in this repository. Review the source before accepting the install; the CLI's official documentation also describes anonymous telemetry and the `DISABLE_TELEMETRY=1` opt-out.

### Shared direct install

Current Codex, Copilot CLI, OpenCode, Gemini CLI, and Pi documentation all recognize `~/.agents/skills/` as a global Agent Skills location:

```sh
git clone https://github.com/squizzeak/adaptive-storage.git
mkdir -p ~/.agents/skills
cp -R adaptive-storage/skills/adaptive-storage adaptive-storage/skills/storage-init ~/.agents/skills/
```

If either destination folder already exists, use the update procedure in the [installation guide](docs/install.md) instead of copying over it; some `cp` implementations would nest the new folder inside the old one.

Claude Code's documented personal location is `~/.claude/skills/`; copy both skill folders there instead. Pi can alternatively install the Git package directly:

```sh
pi install https://github.com/squizzeak/adaptive-storage
```

See the [complete installation guide](docs/install.md) for host-specific invocation, bootstrap instructions, updates, and removal. The guide explains how to add a short global routing instruction because global installation makes a skill discoverable but cannot guarantee that every new session invokes it.

## Global first run

Run setup explicitly the first time you want persistent storage behavior:

- Codex direct install: `$storage-init`
- Codex plugin: open the `$` skill picker and select the combined identity `adaptive-storage:storage-init`, or ask Codex to use that skill
- Claude Code direct install: `/storage-init`
- Claude Code plugin: `/adaptive-storage:storage-init`
- GitHub Copilot CLI direct install: `Use the /storage-init skill`
- GitHub Copilot CLI plugin: `Use the /adaptive-storage/storage-init skill`
- Pi: `/skill:storage-init`
- OpenCode native adapter: `/storage-init`
- OpenCode skill-only or Gemini CLI: `Use the storage-init skill`

Setup does four things:

1. It inventories only the relevant capabilities exposed in the current session. Installed but inaccessible, read-only, temporary, and unverified capabilities remain labeled accurately.
2. It compares eligible arrangements for tasks, notes, and artifacts, including durability, sharing, fidelity, history, conflicts, access boundaries, and likely call overhead.
3. It recommends an arrangement and asks you to choose before establishing new destinations. You may accept global defaults, a binding for only the current project, or both; silence is not treated as acceptance.
4. It saves only the accepted scopes in authorized durable storage, reads them back when possible, and does not migrate existing records.

In filesystem-capable environments, the portable policy convention is `$XDG_CONFIG_HOME/adaptive-storage/config.json`, falling back to `~/.config/adaptive-storage/config.json`. `ADAPTIVE_STORAGE_CONFIG` can point to a different exact file. Restricted or remote hosts can use another authorized durable record and a discoverable non-secret locator.

The sample [`examples/global-policy.json`](examples/global-policy.json) and [`examples/project-policy.json`](examples/project-policy.json) files illustrate policy shape. They are not executable settings consumed by a bundled service, and they contain no real account or project data.

After setup, `adaptive-storage` reuses the accepted global defaults and project overrides. Invoking it in a project with no applicable accepted route starts the same setup flow automatically. A project-only acceptance remains valid for that project even when no global defaults exist, so later sessions there do not repeat global setup prompts. It does not require a background process.

## How storage is organized

Adaptive Storage separates content semantics from storage roles. A single engine can fill several roles, or different engines can be selected for each role and content type.

### Project roles

| Role | Meaning |
| --- | --- |
| **Working** | Editable context and drafts. The policy records whether this location is temporary or durable. |
| **Durable** | Canonical complete records that survive sessions. |
| **Shared** | A canonical remote destination or explicit replica available to its intended collaborators. |
| **Archive** | Optional historical snapshots. An archive does not replace required active records. |

Roles are logical tiers, not claims about vendor performance or service guarantees. A project can use a durable local working set, a remote issue tracker for tasks, a document store for notes, and a file service for binary artifacts. A project override can change one route while inheriting the rest of the global policy.

### Tasks, notes, and artifacts

| Content | What must be preserved | Typical route decision |
| --- | --- | --- |
| **Tasks** | Stable identity, title, state, project, useful priority or due information, relationships, and provenance | Use a native task or issue tracker when its fields are available; otherwise use an agreed structured durable record without silently dropping status or deadlines. |
| **Notes and context** | Complete retrievable text, stable identity, scope, source or revision, and links | Markdown is a portable working form only when conversion preserves enough fidelity. Native comments, tables, and structure stay native when a text conversion would lose them. |
| **Artifacts** | Original bytes or native object, filename, type, size, stable locator, and relationship to the task or note | Use a destination that actually supports the file or native object. A link or summary in a note is an index, not the artifact itself. |

Artifact subtypes can route differently. A project might keep PDFs in a file service while editable slide decks remain in a native presentation platform. Unsupported types stay unresolved until you approve a suitable fallback; the workflow does not silently encode binaries into notes or replace editable files with screenshots.

## How project work flows

On relevant session entry, `adaptive-storage` resolves the workspace identity, reads the saved global policy and project binding, validates only the selected engines needed for the task, inspects pending work, and refreshes relevant changed context. It does not scan every connected account.

During work, it keeps canonical records distinct from working copies, caches, indexes, summaries, and links. Existing project routes remain authoritative until you authorize a change. Global-default changes apply to new unbound projects and do not silently migrate existing records.

At the configured completion point, it publishes only the scoped changes and attempts an exact readback. The reported storage result is one of:

- saved locally;
- committed locally;
- published and verified;
- published but unverified;
- partial;
- conflicted; or
- unsaved and pending.

Task execution and storage publication are separate outcomes. If a task depends on an artifact and artifact publication fails, the workflow does not call the shared task complete.

## Examples

Set a global preference but bind one project's tasks elsewhere:

> Use storage-init. Prefer durable local working notes and publish completed notes to my approved shared notes destination. For this repository only, use its existing issue tracker for tasks. Leave large artifact routing unresolved until one appears.

Resume persistent work:

> Use adaptive-storage to refresh this project's relevant context, show pending tasks, and continue the highest-priority item.

Change a route without moving history:

> Use storage-init to change the artifact destination for new files in this project. Show the routing delta first. Do not migrate existing artifacts.

Request a verified publication:

> Save this report through the project's configured artifact route, link it from the related task, and report whether the final object was read back and verified.

## Limitations

- **Instructions are not enforcement.** A skill guides the agent but does not create platform-level access controls, locks, transactions, or retention policy.
- **Installation is not invocation.** A host may discover a global skill and still fail to select it for a vague request. Use `storage-init` explicitly once and add the documented global routing instruction if you want consistent preflight behavior.
- **No storage backend is included.** The workflow can use only capabilities the current host exposes and the user has authorized. Installing the plugin does not install or authenticate a connector.
- **No universal sync engine exists.** Refresh and publication happen through the active agent session. There is no hidden daemon, close-event hook, scheduler, or promise to sync after the session ends.
- **Concurrency guarantees depend on the backend.** Revision guards, conditional writes, exclusive creation, transactions, and complete readback are used only when the selected engine exposes them. Read-before-write reduces mistakes but cannot eliminate races.
- **Multiple destinations are not atomic.** Each target has a separate result and receipt. Partial success is reported rather than disguised as one successful transaction.
- **No automatic migration or deletion occurs.** Changing a route is prospective unless you separately authorize a scoped migration. Source deletion, force pushes, public sharing, and new audiences require their own authority.
- **Configuration is not automatically shared across devices.** Installing the same skills on two machines does not synchronize their policy. Cross-host policy sharing needs a durable location that each host can actually access.
- **Host and organization policy still apply.** Managed settings, trusted-project rules, sandboxing, cloud-session differences, tool permissions, and provider limits can narrow what is available.
- **Performance statements are design expectations.** Local working sets and change-only refreshes should reduce remote calls, but the project publishes no universal latency or throughput benchmark.

See [Design and boundaries](docs/architecture.md) and [Privacy and data flow](PRIVACY.md) for the full model.

## Verification status

This matrix separates documentation and package-shape checks from live end-to-end host tests.

| Host | Vendor path and command checked against current primary docs | Repository package route present | Live install tested in this release | Fresh-session automatic invocation tested |
| --- | --- | --- | --- | --- |
| Codex / ChatGPT desktop | Yes; CLI `plugin add` also checked in Codex CLI 0.155.0 | `.agents/plugins/marketplace.json` plus Agent Plugins package | Not yet | Not yet |
| Claude Code | Yes | `.claude-plugin/marketplace.json` plus Claude-compatible manifest | Not yet | Not yet |
| GitHub Copilot CLI | Yes | Claude-compatible marketplace plus portable Agent Plugins manifest | Not yet | Not yet |
| OpenCode | Yes | Optional native adapter, direct skills, or community Skills CLI | Adapter runtime smoke tested on 1.18.30; see validation record | Hook injection tested; real model storage workflow not yet tested |
| Pi | Yes | `package.json` declares both canonical skills through `pi.skills` | Not yet | Not yet |
| Gemini CLI | Yes | Direct `~/.agents/skills` or native skill-folder install | Not yet | Not yet |

“Path and command checked” means the host's current official documentation names that location or mechanism. It does not mean every client version, account policy, or execution surface was exercised. The detailed source record is in [Platform sources and compatibility notes](docs/platform-sources.md).

For a real host verification, check five separate states: both skills are installed, both are discoverable, the intended skill is invoked, setup is durably initialized, and a later task can read and update the selected project storage. The installation guide provides host-specific checks.

## Documentation

- [Installation and first-use setup](docs/install.md)
- [Global activation instruction](docs/global-bootstrap.md)
- [Design and boundaries](docs/architecture.md)
- [Primary platform sources and compatibility notes](docs/platform-sources.md)
- [Privacy and data flow](PRIVACY.md)
- [Changelog](CHANGELOG.md)

## Privacy and license

Adaptive Storage collects no telemetry and has no mandatory external destination. Storage content, policies, receipts, and credentials do not belong in this public distribution repository. Review the [privacy notes](PRIVACY.md) and the policies of your agent host and chosen storage providers.

The project is licensed under the [MIT License](LICENSE).

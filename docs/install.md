# Installing Adaptive Storage

Adaptive Storage is an instruction-only, two-skill package:

- `storage-init` is the explicit setup entry point.
- `adaptive-storage` applies the saved policy during persistent project work and runs the same setup flow automatically if configuration is still missing.

Neither skill requires a daemon, an MCP server, an API key, a model provider, a package runtime, or a background hook. The package creates storage configuration only when one of the skills is invoked.

The public repository is [`squizzeak/adaptive-storage`](https://github.com/squizzeak/adaptive-storage).

## Contents

- [Choose an installation route](#choose-an-installation-route)
- [Marketplace installation](#marketplace-installation)
- [Direct global installation](#direct-global-installation)
- [Platform-specific alternatives](#platform-specific-alternatives)
- [Add a routing instruction](#add-a-routing-instruction)
- [Run the first-use setup](#run-the-first-use-setup)
- [Verify the installation](#verify-the-installation)
- [Update or remove](#update-or-remove)

## Choose an installation route

| Route | Best for | What is installed |
| --- | --- | --- |
| Native marketplace | Codex, Claude Code, or Copilot CLI users who want the host to track an installable plugin | The skill-only plugin under `plugins/adaptive-storage/` |
| Community skill installer | OpenCode users who want a package manager to place both skills in OpenCode's global skill directory | Both canonical skills, selected from the public Git repository |
| Shared global folder | People who use several compatible hosts on one machine | Both canonical folders copied under `~/.agents/skills/` |
| Host-specific folder | One host, or a host that does not scan `~/.agents/skills/` | Both canonical folders in that host's user skill directory |

The canonical sources are `skills/storage-init/SKILL.md` and `skills/adaptive-storage/SKILL.md`. The plugin bundle contains generated copies of both for installation; it does not add an MCP or other runtime dependency. Install both siblings. `storage-init` deliberately reads setup guidance from the adjacent `adaptive-storage` skill, so a one-file or one-folder partial install is incomplete.

## Marketplace installation

### Codex and the ChatGPT desktop app

Register the repository's native Codex marketplace:

```sh
codex plugin marketplace add squizzeak/adaptive-storage
codex plugin add adaptive-storage@adaptive-storage
```

The second command is exposed by Codex CLI 0.155.0. If your client does not offer `codex plugin add`, restart the ChatGPT desktop app, open the Plugins Directory, select the **Adaptive Storage** source, and install **Adaptive Storage** there. Current OpenAI web documentation describes `codex plugin marketplace add` as catalog registration and directs local plugin installation and testing through the desktop app.

The catalog is [`../.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json). The plugin is skill-only: installation does not ask you to configure an MCP connection or provider.

### Claude Code

Claude Code can add the repository's native marketplace and install the plugin at user scope:

```sh
claude plugin marketplace add squizzeak/adaptive-storage
claude plugin install adaptive-storage@adaptive-storage
```

Start a new Claude Code session after a shell-level install. In an existing interactive session, `/reload-plugins` can apply a newly installed plugin. Plugin skills are namespaced, so setup is `/adaptive-storage:storage-init` and the operational workflow is `/adaptive-storage:adaptive-storage`.

### GitHub Copilot CLI

Copilot CLI recognizes the Claude-compatible marketplace included in this repository:

```sh
copilot plugin marketplace add squizzeak/adaptive-storage
copilot plugin install adaptive-storage@adaptive-storage
```

The first command registers the catalog; the second installs its plugin for the current user. Copilot CLI officially checks `.claude-plugin/marketplace.json` as a compatible marketplace location.

## Direct global installation

Codex, Copilot CLI, OpenCode, Gemini CLI, and Pi all document `~/.agents/skills/` as a user-level Agent Skills directory. One copy there can serve all five hosts:

```sh
git clone https://github.com/squizzeak/adaptive-storage.git
mkdir -p ~/.agents/skills
cp -R adaptive-storage/skills/adaptive-storage adaptive-storage/skills/storage-init ~/.agents/skills/
```

Review both `skills/adaptive-storage/SKILL.md` and `skills/storage-init/SKILL.md` before copying them. Agent Skills are instructions given to an agent and should be treated as executable trust material even when, as here, they contain no bundled executable.

If either destination folder already exists, compare or remove that specific old copy before installing an update. Do not run the copy command over existing folders: some `cp` implementations will create unwanted nested directories.

### Claude Code direct install

Claude Code's documented personal skill directory is `~/.claude/skills/`:

```sh
mkdir -p ~/.claude/skills
cp -R adaptive-storage/skills/adaptive-storage adaptive-storage/skills/storage-init ~/.claude/skills/
```

Claude Code normally notices changes inside an existing skills directory during a session. If the top-level `~/.claude/skills/` directory did not exist when the session started, restart Claude Code.

## Platform-specific alternatives

### Codex

For local authoring, current Codex documentation uses `~/.agents/skills/<skill>/SKILL.md` at user scope and `.agents/skills/<skill>/SKILL.md` at repository scope. You can also ask the built-in `$skill-installer` to install both skills from this repository. If newly installed skills do not appear, restart Codex.

### GitHub Copilot CLI

Copilot CLI can manage personal skills with `copilot skill add`, and its personal skill directories are `~/.copilot/skills/` and `~/.agents/skills/`. Because Adaptive Storage contains two related skills and supporting files, install both complete directories rather than raw `SKILL.md` URLs. Copilot's plugin-qualified syntax uses `/adaptive-storage/storage-init`; its direct-skill syntax uses `/storage-init`.

### OpenCode

Use the shared `~/.agents/skills/` installation above, or copy **both** `skills/adaptive-storage/` and `skills/storage-init/` into `~/.config/opencode/skills/`. OpenCode documents native skill discovery from both locations.

Vercel's community `skills` CLI also targets OpenCode's documented global directory and can select both skills from this public Git repository:

```sh
npx skills add squizzeak/adaptive-storage -g -a opencode --skill adaptive-storage --skill storage-init
```

Review the skills before accepting the install. The CLI's official documentation says it collects anonymous telemetry by default and supports the `DISABLE_TELEMETRY=1` environment variable to opt out.

The `skills` CLI and skills.sh directory form a community ecosystem rather than an OpenCode-native marketplace. OpenCode's own npm plugin mechanism is a different system. This repository does not claim that OpenCode understands the Codex or Claude marketplace manifests, and their marketplace commands do not apply to OpenCode.

### Pi

Pi supports the shared `~/.agents/skills/` path. It can also install this repository as a Pi package because Pi discovers conventional `skills/` directories in Git-backed packages:

```sh
pi install https://github.com/squizzeak/adaptive-storage
```

This is Pi's Git package manager, not a universal Agent Skills marketplace.

### Gemini CLI

Gemini CLI supports `~/.agents/skills/` as an alias for its native `~/.gemini/skills/` user directory. The shared installation above is therefore the simplest multi-host route. Gemini's `gemini skills install` command is a native skill installer, while Gemini Extensions are a separate packaging system; this repository does not claim to be a Gemini Extension.

Gemini asks for consent when a remote skill is installed and again when a skill is activated. Installation alone does not grant activation.

## Add a routing instruction

Being installed means a host can discover the skill. It does not guarantee that every new session will choose it. Skill selection depends on the request, the skill description, host policy, and available context. Add this short instruction to your host's global instruction file if you want consistent routing:

> For project task tracking, durable project notes, or retained artifacts, load and follow the `adaptive-storage` skill. If the current project has no applicable accepted storage route, run the `storage-init` setup flow first. Both skills share the same accepted configuration.

Append or merge that text into the existing file; do not overwrite unrelated instructions.

| Host | Global instruction file |
| --- | --- |
| Codex | `~/.codex/AGENTS.md` (or `$CODEX_HOME/AGENTS.md`) |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` (or `$COPILOT_HOME/copilot-instructions.md`) |
| Claude Code | `~/.claude/CLAUDE.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` |
| Pi | `~/.pi/agent/AGENTS.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` |

These are instruction files, not installers. They help the host route relevant requests to a skill that must already be installed.

## Run the first-use setup

Open a session in the project you want to manage and invoke the skill explicitly once:

| Host | First-use request |
| --- | --- |
| Codex, direct skills | `$storage-init Set up global storage defaults and bind this project.` |
| Codex, plugin | Open the `$` skill picker, select `adaptive-storage:storage-init`, and request: `Set up global storage defaults and bind this project.` |
| Claude Code, direct skills | `/storage-init Set up global storage defaults and bind this project.` |
| Claude Code, plugin | `/adaptive-storage:storage-init Set up global storage defaults and bind this project.` |
| GitHub Copilot CLI, direct skills | `Use the /storage-init skill to set up global storage defaults and bind this project.` |
| GitHub Copilot CLI, plugin | `Use the /adaptive-storage/storage-init skill to set up global storage defaults and bind this project.` |
| Pi | `/skill:storage-init Set up global storage defaults and bind this project.` |
| OpenCode, Gemini CLI | `Use the storage-init skill to set up global storage defaults and bind this project.` |

`storage-init` is a convenient explicit entry point, not a separate runtime. Invoking `adaptive-storage` for persistent work with no completed configuration runs the same first-use setup. There is no bootstrap program and no daemon or hook that needs to remain running.

The initial setup can establish user-level defaults, bind only the current project, or do both, according to what you accept. Later projects inherit accepted global defaults unless you approve a project override. A project-only acceptance completes setup for that project and does not create a global completion marker; later sessions in the same project should reuse its binding without repeating global prompts. A global installation only makes the skills discoverable; it does not itself create configuration or share project records.

## Verify the installation

Use the host's own inventory where one is documented:

- **Codex:** type `$` or run `/skills`, then look for both `storage-init` and `adaptive-storage`. For a marketplace install, confirm the plugin in the desktop Plugins Directory.
- **Claude Code:** run `/skills` and confirm both skills; plugin installs appear under their plugin namespace.
- **GitHub Copilot CLI:** run `copilot skill list` for a direct install and confirm both skills, or `copilot plugin list` for a marketplace install.
- **OpenCode:** ask it to list available skills, or make an explicit first-use request and confirm that it loads `adaptive-storage` through the native `skill` tool.
- **Pi:** confirm and run `/skill:storage-init`; Pi also reports discovered-skill conflicts or validation problems at startup.
- **Gemini CLI:** run `/skills list`, confirm both skills, then invoke `storage-init` and approve activation when prompted.

Discovery is only the first check. Complete verification means invoking the skill in a disposable project, completing its first-use setup, and confirming that the accepted policy was read back and the chosen local or remote destinations contain the expected records, fields, and artifacts.

## Update or remove

Marketplace installs should use their host's marketplace or plugin update command. Direct copies are updated by replacing only the installed `adaptive-storage` and `storage-init` folders with fresh copies of both canonical folders from a reviewed checkout.

Removing the global skill does not remove records already written to local files, repositories, task systems, document stores, or artifact services. Those records remain subject to their destination's own retention and access rules until you deliberately archive or delete them there.

For the evidence behind each platform path and command, see [Platform sources](platform-sources.md).

# OpenCode adapter

This optional native plugin registers `/storage-init`, makes both bundled skills
discoverable, and appends a compact storage-routing instruction to model turns that
have a session ID. The portable skills work independently of this adapter.

It uses OpenCode's `config`, `experimental.chat.system.transform`, and
`experimental.session.compacting` hooks. The experimental hooks are version-sensitive;
consult the verification record below when upgrading OpenCode.

## Install globally from a checkout

Clone the complete repository to a stable location. Keep `adapters/` and `skills/`
in the same checkout; moving only `index.mjs` will fail with an incomplete-package
error. In your global `~/.config/opencode/opencode.json`, merge this entry into the
existing `plugin` array, replacing the illustrative path with your checkout's actual
absolute file URL:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "file:///absolute/path/adaptive-storage/adapters/opencode/index.mjs"
  ]
}
```

Preserve existing plugins and other configuration. Use a correctly URL-encoded file
URL for paths containing spaces; a JavaScript `pathToFileURL` conversion can generate
one. Restart OpenCode, verify both skills are available, and run `/storage-init`.
The adapter modifies the resolved configuration in memory; it does not rewrite
OpenCode's configuration or your storage policy on disk.

For project-only installation, add the same entry to that project's `opencode.json`
instead. Do not commit personal absolute paths into a shared repository. Use a local
untracked config or the global installation when the checkout path is machine-specific.

An alternative is a global JavaScript shim in
`~/.config/opencode/plugins/adaptive-storage.js` that re-exports the plugin from its
complete checkout:

```js
export { default } from 'file:///absolute/path/adaptive-storage/adapters/opencode/index.mjs';
```

Use one installation method to avoid duplicate plugin loading. No npm registry
publication is claimed. The repository's package entry point and `npm pack` layout
also include the adapter and both skills; the package remains private to prevent
accidental registry publishing. The installed skill-only marketplace ZIP does not
contain this optional adapter.

## Options

OpenCode versions supporting plugin option tuples can configure:

```json
{
  "plugin": [
    [
      "file:///absolute/path/adaptive-storage/adapters/opencode/index.mjs",
      { "automatic": false, "commandName": "adaptive-storage-init" }
    ]
  ]
}
```

- `automatic` defaults to `true`. It adds routing instructions to session model
  calls and a preservation reminder to compaction context. `false` retains skill
  discovery and the explicit command without those automatic prompts.
- `commandName` defaults to `storage-init`. Existing commands are preserved. If
  another command already owns that name, use an explicit alternative such as
  `adaptive-storage-init`, or invoke the `storage-init` skill directly.

No agent, model, permission, existing skill path, or existing command is overridden.
The skill tool remains subject to OpenCode's permission settings. A conflicting
same-name skill installation should be removed or reconciled by the user rather
than silently overridden.

## What automatic means

The hook also runs for session-associated auxiliary requests such as title generation;
a session ID is not a main-response-only filter. The reminder is advisory and never
starts another model request.

The plugin ensures its routing reminder is added when the supported model hook
runs. The agent still decides whether a request needs persistent context and follows
the shared skill. On first applicable use, it presents storage choices and obtains
selection. Existing accepted configuration is reused. Installation and startup do
not choose an engine, initialize a policy, or migrate existing content.

There is no `session.idle` publisher, event-driven storage mutation, background
model call, injected user message, or connector client. Sync occurs through the
agent's normal tools and configured completion policy. Compaction preserves a
reminder to retain already-known policy/pending state; it never invents state or
replaces the host's compaction prompt. A host custom compaction prompt may ignore
additional context, according to OpenCode's own hook semantics.

## Verification

Run `node --test tests/opencode.test.mjs` from the repository root. Tests cover config
preservation, repeated hook calls, command collisions, automatic opt-out, auxiliary
calls, compaction prompt preservation, no side-effect hooks, invalid options, and
relocated/partial packages. See the repository [validation record](../../docs/validation.md)
for actual host verification and its limits.

Sources: [OpenCode plugins](https://opencode.ai/docs/plugins/),
[configuration schema](https://opencode.ai/config.json),
[plugin hook types](https://github.com/anomalyco/opencode/blob/v1.18.30/packages/plugin/src/index.ts),
and [custom commands](https://opencode.ai/docs/commands/).

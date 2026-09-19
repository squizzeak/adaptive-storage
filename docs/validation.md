# Validation record

Initial validation date: 2026-09-19.

## Automated package checks

The maintainer suite checks that both skills and all referenced local resources are
present, generated copies match canonical sources, marketplace paths and manifest
identities agree, and the marketplace skill-only bundle has no executable or MCP dependency.
Seven packaging regressions cover missing siblings, stale generated content,
unexpected bundled files, source/output symlinks, reproducible complete archives,
and preservation of existing archive files. Run the commands in [AGENTS.md](../AGENTS.md)
to reproduce these checks; the GitHub Actions workflow runs the same suite.

The bundled Skill Creator validators accepted both skill entrypoints, and the
Plugin Creator validator accepted the Codex compatibility package. Those validators
were run in a temporary maintainer environment; their YAML dependency is not part
of the installed skills.

## Independent behavioral evaluation

A separate agent performed a read-only, instruction-following simulation with
fictional capabilities, without changing any real account or record:

| Fixture | Observed response |
| --- | --- |
| Unconfigured session with local files, text connector, and private Git remote | Compared arrangements and requested user selection before establishing routes |
| PPTX needed but only text-note route approved; working files temporary | Kept publication pending and proposed a scoped file-capable alternative |
| Note-create timeout resolved by stable ID; required binary still failed | Avoided duplicate note creation and kept dependent task incomplete |
| Saved global policy inaccessible; unpublished local notes present | Preserved pending work and did not replace the global authority |

The evaluation identified two ambiguities, corrected before publication: references
can be loaded through host resource tools rather than only filesystem paths; and
project-only acceptance completes project setup without creating global defaults.
It also prompted clearer wording that even a sole eligible global destination needs
acceptance when no prior choice exists.

These are behavioral simulations, not live connector concurrency tests. The full
scenario inventory in [tests/scenarios.md](../tests/scenarios.md) includes additional
acceptance cases that remain for host-specific testing.

## Installation evidence

Platform documentation sources are recorded in [platform-sources.md](platform-sources.md).
Local command help was inspected for Codex CLI 0.155.0 and OpenCode 1.18.30. No claim
of a live installation, fresh-session automatic invocation, or public marketplace
listing approval follows from documentation, packaging checks, or command help.


## OpenCode adapter 0.2.0

Nine Node regression tests cover config preservation, idempotent hook execution,
command collisions, automatic opt-out, calls without a session, compaction prompt
preservation, the absence of side-effect hooks, invalid options, and complete versus
partial relocated packages. They use a host context that throws on any SDK access.
The package archive was inspected for the adapter and both sibling skills; the
extracted adapter successfully initialized and registered its command and skills.
These checks use built-in Node APIs and introduce no installed runtime dependency
into the portable skills. CI runs the Node suite alongside the seven Python
packaging regressions.

The actual adapter was loaded by installed OpenCode **1.18.30** in isolated
configuration, cache, state, and data directories. Project configuration, external
skill discovery, and default plugins were disabled for the check; the user's global
configuration was not changed. `debug config` showed the `storage-init` command and
bundled absolute skill path. `debug skill` resolved both actual skill entrypoints.

A localhost-only OpenAI-compatible test server returned canned responses. OpenCode
sent two requests (main response and title generation); each contained the adapter
routing marker exactly once. With the `automatic: false` option tuple, neither
request contained the marker. The actual compaction hook was also called directly:
it added context only with automatic routing enabled.

This verifies host loading, discovery, option handling, and system-hook execution.
It does not verify a real model's skill adherence, accepted storage setup, live
connector synchronization, or end-to-end host compaction. The system and compaction
hooks remain experimental and should be checked when upgrading OpenCode. The hook
may run on session-associated title/summary requests as well as the principal turn.

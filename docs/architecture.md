# Design and boundaries

Adaptive Storage is a pair of portable Agent Skills. `storage-init` is the explicit
setup entry point; `adaptive-storage` handles discovery, first-use setup, session
refresh, routing, and completion-time publication. Both read the same policy.

The host provides tools. The agent inspects their schemas and maps supported
operations to the workflow. There is no bundled adapter daemon, server, network
client, hidden account, mandatory Git executable, or mandatory MCP connection.
Optional marketplace manifests distribute the same skills without adding runtime tools.
The separate OpenCode adapter adds skill discovery, an explicit setup command, and
system/compaction routing reminders. It does not implement storage operations,
initialize policy at startup, or publish on idle events.

## Decision model

The policy chooses by actual capability, user preference, existing destination,
content semantics, and scope before performance. Working, durable, shared, and
archive roles can reside in one or several engines. Tasks, notes, and artifact
subtypes can use different routes. Unsupported formats trigger an approved fallback
or an explained choice; a note link never substitutes for missing artifact bytes.

## Configuration hierarchy

Current explicit instructions and domain constraints take precedence. Project
bindings override global defaults field by field. Lists replace lists; omitted
fields inherit; null disables a role. Defaults apply to new unbound projects;
changing a default does not migrate existing records. Examples are illustrative
policy shapes, not executable settings consumed by a bundled service.

## Performance

Prefer a persistent local working set where available, fetch scoped changes on
entry, edit locally, and publish only changes at agreed completion points. Cache
capability evidence and policy decisions; avoid account-wide startup scans.
Performance gains are expected from fewer remote calls, not benchmarked guarantees.
Without a cheap change listing, freshness and latency remain a tradeoff exposed to
the user. A temporary workspace requires earlier durable checkpoints.

## Consistency

Compare local and remote versions against the last synchronized base. Preserve
conflicts. Use provider revision guards where available. Without them, read-before-
write and readback do not eliminate races. Operation identity and receipts help
recover uncertain writes but cannot manufacture exactly-once semantics.

Multi-destination publication has per-target receipts and can partially succeed.
Only one canonical authority is configured per collection; editable replicas need
an explicit reconciliation path. Git commits, pushed branches, merged changes, and
verified artifact bytes are separate states.

## Portability and limitations

First activation starts setup; skill files do not execute during installation.
Global host instructions request ongoing activation. Cross-host sharing of policy
requires a durable location each host can actually access. Installing the same skill
on two computers does not synchronize their configuration.

Domain rules can prohibit drafts or require immutable records. Those rules also
apply to local storage. This general-purpose skill does not copy Mood Journal's
clinical behavior or impose journal-only constraints on ordinary project documents.
It adopts capability discovery and honest persistence boundaries as design lessons.

## Future extensions

If real usage shows a need, optional deterministic helpers can handle hashing,
policy validation, or repetitive engine operations. A dedicated sync service could
add scheduling or coordination. Neither is implied by the current release.

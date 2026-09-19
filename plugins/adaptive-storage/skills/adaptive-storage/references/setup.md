# First-use setup

Run setup automatically on the first applicable invocation when no completed policy is found. Setup is conversational, not an install-time executable. Do not obstruct unrelated disposable work. See [configuration](configuration.md) for discovery and persistence.

## Inventory first

Discover session capabilities through exposed tool metadata and small relevant read-only checks. Do not scan every account, project, or private document. Confirm known endpoints and permissions only as needed. Use [discovery](discovery.md). If tools are deferred, search for the needed capability before declaring it absent.

## Present arrangements

Offer a compact comparison of eligible arrangements, not a list of brand names. Include:

- Working location and durability of its drafts.
- Authoritative destination for tasks, notes, and artifacts.
- Whether sharing occurs immediately or on completed work/checkpoints.
- Cross-agent reach and any required connections.
- Supported artifact types/limits and how unsupported types would be handled.
- History, conflicts, and verification limitations.

State a recommendation in terms of the user's priorities. Label performance expectations as estimates unless measured. Even a sole eligible option needs acceptance if it establishes new global destinations. Existing explicit choices count as acceptance.

Ask one focused question at a time or a short selection menu. Offer “use this workspace only” and “save as my default for new projects.” The user can choose different destinations per content type, local-only, remote-direct, or automatic selection within named authorized destinations. Never suggest public storage for private content without an explicit audience choice.

A workspace-only selection completes that project's setup, not global setup. Record the accepted scope in the project policy and do not create a global complete marker or infer defaults for other projects. Subsequent sessions in the same project reuse its policy without asking for global setup again. A new unbound project can offer global defaults or another project-only choice.

## Establish a concrete policy

Resolve global preference scope, working-copy policy, exact destination identities, eligible fallback destinations, and publication timing. Global preferences may name engine families and selection criteria without giving blanket write authority to every project in an account. Project binding supplies the exact collection/repository/path, audience, and content scope.

Default proposal: reuse durable local working files when available; refresh relevant changes on session entry; publish completed task work; preserve pending changes on failure. Projects can choose checkpoints or direct remote writes. No hidden daemon or app-close detection is promised.

Capture task/notes/artifact routes independently. If not currently needed, leave an artifact subtype unresolved until it arises rather than forcing choices about every conceivable format. A route marked unresolved must be resolved before a dependent publication.

## Persist and verify

Save accepted policy in authorized user-scoped storage outside the distributed skill and outside public project history. Follow host permissions. Record schema version, policy ID/revision, accepted scope, routes, preference provenance, verification level, and setup completion. Do not persist secrets or a guessed account identity.

Read back the policy. Mark setup complete only after a verified durable policy write, or disclose weaker verification. If only session retention exists, state that future sessions may need configuration again. A partially completed setup resumes from accepted fields and asks only unresolved questions. Never repeat a successful create after an uncertain response without locating its stable policy ID.

Do not migrate existing records during setup unless the user has requested a scoped transfer. New defaults govern new unbound workspaces. Existing project routes stay in effect until explicitly changed.

## Global activation

A globally installed skill is discoverable across projects, subject to host support. It is not guaranteed to load for every prompt. Installation instructions provide a host-level routing instruction asking the agent to load this skill for persistent work at session entry and completion. First invocation always checks setup even when the user did not separately request configuration. Do not claim the bootstrap instruction enforces execution or changes host retention.

# Global policy and project configuration

Configuration is storage-neutral. Use an existing authorized user-scoped record if available. In filesystem environments, the proposed portable convention is `$XDG_CONFIG_HOME/adaptive-storage/config.json`, or `~/.config/adaptive-storage/config.json` when XDG_CONFIG_HOME is unset. These are this skill's conventions, not host-provided APIs. On other systems or restricted hosts, use an approved equivalent or a discoverable pointer to a durable record. Do not write outside authorized roots merely to follow a convention.

The optional environment variable `ADAPTIVE_STORAGE_CONFIG` can identify the exact config file when a host exposes environment access. Otherwise a host global instruction can contain the non-secret policy locator. Validate the locator and scope; never execute its contents. Do not enumerate unrelated home directories or remote records to hunt for preferences.

Global configuration belongs outside the skill installation: upgrades and marketplace caches may replace installed files. No credentials, tokens, personal source content, or private inventory belongs in the distribution repository.

## Global model

Store the logical fields below in the engine's supported representation. JSON is a convenience, not a runtime dependency:

- `schema_version`, stable `policy_id`, `revision`, and `setup_state` (incomplete or complete).
- Scope of accepted preferences and configuration provenance.
- `selection_mode`: user-selected or automatic-within-approved-scope.
- `allowed_destinations`: opaque IDs mapped to exact non-secret engine/account/root locators and approved audiences; unknown capability fields remain unknown.
- `defaults`: working-storage preference, publication trigger, freshness requirements, and routes per content type.
- Route fields: working, canonical, optional replicas, allowed fallbacks, supported subtypes, and verification/preservation requirements.
- A private mapping of stable workspace IDs to project policy locators where necessary.

A preference for “Git” is not permission to use every configured remote. Bind account, repository, branch policy, path scope, and visibility for each project. Shared/global records visible to several agents require the same conflict-aware update protocol as content records.

## Project binding and overrides

On first project use, identify it from host context and existing policy. A Git URL or filesystem path is a locator, not immutable identity. Store a stable workspace ID; retain mappings on rename or move. Distinct clones may deliberately share a workspace identity; branch-local drafts still need separate working-copy IDs. Ask if identity is ambiguous rather than merging projects.

A project policy can live in an authorized `.adaptive-storage/project.json`, a private central mapping, or a native scoped record. Do not automatically commit private locators. A shared sanitized project policy may be versioned when intended.

Resolve effective configuration as follows:

1. Explicit current user instruction and applicable host/domain constraints.
2. Project overrides for the specified content type, subtype, and role.
3. Saved global defaults for otherwise unbound fields.
4. A proposed selection requiring acceptance where material fields remain unresolved.

Merge object fields; replace lists rather than combining them implicitly. Omitted means inherit. Explicit null means disabled, not “pick another destination.” A canonical null means no configured publication destination, never permission to claim a record published. Reject unknown schema versions or conflicting authority declarations without silently resetting configuration.

Project overrides may change performance tiers, freshness, and publication cadence within already authorized scope. A new destination/audience needs user selection unless included in an explicit automatic-selection policy. Existing project bindings do not silently change when global defaults change.

## Logical tiers

- **Working:** editable context and drafts; record whether storage is temporary or durable.
- **Durable:** canonical complete records that survive sessions.
- **Shared:** canonical remote or explicit replicas accessible to intended collaborators.
- **Archive:** optional retained historical snapshots; never a substitute for required active records.

Tiers describe roles, not vendors or guaranteed service levels. Choose independently for tasks, notes, and artifact subtypes. Record one canonical authority per collection; a replica must identify its source and last successful publication.

## Sync state

Track stable record ID, content type, workspace ID, local/remote locators, base revision/hash, pending operation ID, and last verified result. Preserve a base copy or sufficient structured comparison data when possible. Keep status receipts for separate targets; multiple remote writes are not one transaction. Protect private configuration and state from accidental repository publication.

## Policy changes

Show the effective routing delta before changing destinations. Reuse user authorization already given. Retain the old route's pending changes and references. A route change applies prospectively unless a migration is explicitly included. For migration, inventory exact records, copy content and metadata, verify destination fidelity and links, then record cutover. Retain sources by default; source deletion needs its own explicit scope.

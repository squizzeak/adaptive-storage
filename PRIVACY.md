# Privacy and data flow

Adaptive Storage includes instructions, packaging metadata, and an optional OpenCode adapter. It runs no service,
collects no telemetry, and defines no mandatory external destination. Your agent
host and chosen storage providers have their own data handling and retention.

The skill instructs agents to inspect available capabilities, respect established
scope, and ask for storage choices when needed. It can direct tools to read/write
records only within the user's authorized workflow. These instructions are not
platform-enforced access control.

Keep actual policies, account locators, sync receipts, working documents, and
artifacts outside this public distribution repository. Do not put credentials in
configuration. Local files, Git repositories, and cloud stores are not inherently
private or encrypted merely because this skill uses them.

A no-save instruction prevents skill-initiated writes within its scope; it does not
change host-managed conversation retention. No automatic source deletion, public
publication, background scheduling, or connector installation is implied by setup.

The optional OpenCode adapter checks for its packaged skill files and modifies only
resolved in-memory configuration and prompt context. It makes no network requests,
writes no files, and invokes no model or connector itself. The host passes its
routing instructions to the model under the host's existing data handling policy.

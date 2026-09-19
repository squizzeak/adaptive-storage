# Global activation instruction

Install both skills globally using the [installation guide](install.md). Merge the
following paragraph into the host's supported user-level instruction mechanism;
preserve existing instructions. Use the host's namespaced skill name if its plugin
installer requires one.

> At the start of work that needs persistent project context, tasks, notes, or
> artifacts, load the adaptive-storage skill and run its session preflight. If no
> completed storage policy exists, run its first-use setup (also available through
> storage-init), explain the available choices, and obtain my selection. Reuse
> accepted global defaults and project overrides thereafter. Work through the
> selected storage arrangement and run its publication/verification step before
> reporting the applicable unit of work complete. Skip this workflow for disposable
> questions that do not use persistent context. Do not migrate records or add new
> destinations merely because a capability is available.

This is an instruction to the agent, not a startup hook or enforced scheduler.
Global installation alone makes skills discoverable; it does not guarantee every
host will select them automatically. On first use, explicitly invoke storage-init
if the host has not activated the workflow. A fresh-session smoke test is required
before claiming automatic behavior works in a particular host/version.

A non-secret global policy locator can be added to this instruction when useful.
Never embed credentials or private source documents. Configuration belongs outside
the installed skill; marketplace updates can replace installed files.

# Route tasks, notes, and artifacts

Select a destination by content semantics and actual support. The working copy, canonical object, search index, and handoff summary are distinct. A URL to an artifact is not the artifact itself.

| Content | Minimum useful durable representation | Capability-sensitive behavior |
| --- | --- | --- |
| Tasks | Stable identity, title, state, project, relevant priority/due time/relationships, provenance | Prefer selected native task/issue fields when supported. Preserve unsupported fields in a defined metadata sidecar or suggest another tracker. Do not silently drop deadlines or recurrence. |
| Notes/context | Complete text, stable identity, scope, source/revision, links | Markdown is a portable working format when conversion is lossless enough for the task. Preserve source format when comments, tables, or native structure would be lost. |
| File artifacts | Original bytes/native object, filename, type, size, stable locator, relationship to task/note | Use a file-capable destination; verify bytes/checksum if available. A note-only store can hold the index after the artifact is saved elsewhere. |
| Native documents | Native object or faithful export with declared limits | Native edit history, comments, formulas, permissions, or interactive behavior may not survive export. Do not call a text summary a complete copy. |
| Historical records | Required immutable records and linked corrections | Honor the originating workflow's preservation policy. Git history alone does not satisfy a ban on modifying an existing canonical record. |

## Task state

Bind the selected task tracker separately from session planning tools. Agent planning steps can stay transient unless the user/policy requests durable tasks. For durable work, use native status operations or an agreed structured Markdown representation; distinguish open, blocked, completed, and deferred semantics. Preserve provenance and existing IDs. Do not create duplicate tracker entries from every local checklist edit.

Publish required artifacts and notes before marking a task complete when completion depends on them. If execution succeeded but publication failed, report both states. Do not mark the tracker complete with a broken artifact link.

## Unsupported artifacts

Check type/size/API support before uploading. If unsupported, prefer an already approved compatible artifact route. Otherwise explain the concrete mismatch and offer alternatives available in the session: durable local files, an accessible file service, repository/LFS/release storage if suitable, or a native authoring platform. Explain sharing and fidelity tradeoffs. Never silently encode large binaries into note text, discard formulas, or substitute a screenshot for an editable document.

Preserve pending files in authorized durable working storage when possible. If only temporary files are available, disclose their limited lifetime and resolve persistence before claiming completion. Do not promise a later background transfer. Link the verified artifact from the associated note/task and record its actual destination.

## Project tiers

A project can inherit global note storage while overriding tasks to an issue tracker and artifacts to a file service. Subtype routing can send PDFs and editable slide decks to different destinations. A read-only source can be cited or cached with provenance, but cannot serve as the write target. Resolve only the routes needed for current work, while keeping unresolved routes visible.

## Minimal disclosure

Transfer only records in the configured project/content scope. A configured connector may expose an entire account; that does not make its entire inventory project context. Do not move private records into a software repository because the repository happens to be writable. Do not publish local sync caches, private policies, or unrelated staged files with artifacts.

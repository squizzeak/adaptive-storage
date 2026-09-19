# Refresh, edit, publish, recover

Use existing authorized tools. This is an agent-executed protocol, not an automatic transactional sync engine. Record reduced guarantees when an engine lacks revision checks, full readback, stable IDs, or durable state.

## Refresh

1. Resolve the project's canonical routes and existing working-copy state. Recover pending operations before issuing duplicate creates.
2. Enumerate relevant changed records using revision/change listing if available. Paginate completely for the bounded scope. Do not treat a truncated list or missing search result as a deletion.
3. For each candidate, compare the last synchronized base, current local content, and current remote content/revision. Timestamps alone are insufficient conflict evidence.
4. Remote-only changes can refresh an unchanged local copy. Local-only changes remain pending. Identical changes can converge after verification. Changes on both sides require reconciliation; preserve alternatives and do not use silent last-writer-wins.
5. Without efficient change listing, use targeted record retrieval and disclose freshness limits. Do not download the entire account on every session. A user-approved cache window can reduce refresh cost, but time-sensitive task state must meet its configured freshness requirement.

A disconnected session can use authorized cached context with its last verified freshness disclosed. Read-only remote engines can supply context but cannot fulfill a publication route.

## Work and publication boundary

Save local changes only when permitted by the originating workflow. Preserve the base and operation identities. Ordinary project work can checkpoint locally; an explicit no-save or end-only journal policy can prohibit even local drafts.

Publish on the configured trigger: completed unit of work, explicit checkpoint, or direct remote writes. App closing, silence, or a topic change is not a reliably observable trigger. No scheduled execution is created by this skill.

## Publish

1. Determine the exact changed records, metadata, and targets; avoid unrelated files. Assign stable operation/record identities before creates.
2. Re-read remote bases immediately before writes. Use conditional updates/exclusive creation where exposed. If absent, sequential reads and writes reduce mistakes but cannot prevent races. Use a single-writer arrangement, independent immutable records, or report conflicting writes as pending.
3. Preserve complete record metadata when an API uses replacement semantics. Do not send partial objects that clear omitted fields. For immutable records create separately identified linked revisions.
4. Write through the selected tools. After a timeout or ambiguous response, reconcile by stable identity/operation receipt before retrying. No provider idempotency key means no promise of exactly-once creation; ambiguity can require stopping the retry.
5. Retrieve the result and compare intended content, metadata, native fields, and artifact bytes or declared verification evidence. Normalization that changes substantive content is a mismatch, not success. If readback is unavailable, label the write unverified.
6. Advance the base/receipt only for successful verified objects. A weaker user-accepted verification mode must remain explicitly labeled and retain enough pending evidence for later reconciliation. Keep failed targets pending; do not retry successful creates blindly.
7. Confirm exact locators and status. A local file save, remote acknowledgment, and verified publication are distinct outcomes.

## Conflicts and multiple destinations

Separate writers should use separate working copies and common record identity. Do not overwrite a shared file concurrently. Git worktrees/branches can isolate drafts where available. A skill does not supply locks across agents.

One canonical authority per collection avoids circular synchronization. Replicas identify their source and revision. If a replica accepts edits, configure an explicit contribution/reconciliation path before treating it as bidirectionally synchronized. Publish to multiple stores with per-target receipts; partial success is normal and not atomic.

Do not infer deletion from absence. Default to preserving remote and local records; propagate deletion only under an explicit deletion policy with scope and evidence. Keep tombstones/receipts where supported. Never remove source records merely because a mirror exists.

## Recovery

On restart, inspect pending state, remote result, and local artifacts. Resume only incomplete operations. Preserve the original task/session timestamps separately from retry/save time. If a working directory is temporary, copies not durably published may be unrecoverable; report the actual situation without claiming preservation.

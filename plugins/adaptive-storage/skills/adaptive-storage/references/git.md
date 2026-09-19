# Git as working, durable, and shared storage

Use Git only when appropriate tools and an authorized repository are available. A local checkout supplies fast file operations; local commits supply history; a remote adds sharing only after verified publication. No Git executable or repository is required for other storage modes.

## Bind the route

Record repository identity, remote, authorized branch/PR policy, content paths, workspace ID, and intended audience. Verify these from actual repository metadata and platform access where possible. A remote named origin does not prove ownership, privacy, or push authorization. Keep private state separate from public source.

Reuse existing repository conventions. Never initialize inside an unrelated parent repository or collect all project content automatically. A dedicated context repository is an option, not a requirement.

## Refresh and work

Inspect branch and working state before refreshing. Fetch can inspect remote updates without integrating them. Reconcile them while preserving uncommitted work; do not use destructive reset/clean or force-push as sync shortcuts. Branch/worktree isolation is useful for concurrent writers, but resolve how changes reach the canonical branch.

Track only selected documents/artifacts. Stage exact paths and inspect staged changes. Do not sweep unrelated staged work into the storage commit. Hashes and commit IDs are evidence of exact revisions, not proof of remote publication or immutable provider retention.

## Publish

Follow the project's normal commit and review rules. If direct pushes are authorized, push the intended branch and verify the remote commit. If a PR is required, create/update the PR through authorized tools and report submitted/pending integration until merged. A pushed feature branch is not the canonical shared state if readers use main. Never bypass branch protections.

Git text merges can resolve non-overlapping edits but do not prove semantic consistency. Check merged decisions, task state, and references. Preserve conflicts for resolution rather than automatically choosing one side. Binary files often need a separate conflict decision.

## Artifacts and preservation

Check host limits and repository conventions before committing large/binary files. Suggest an authorized file service, Git LFS, or release assets when appropriate; none is presumed installed or configured. Verify LFS/object availability separately from pointer-file commits. A URL or LFS pointer alone does not prove artifact bytes were published.

For immutable-entry workflows, use separate files/records and linked corrections. Replacing a file with a newer version is not append-only merely because Git retains the old commit. No automatic history rewriting, source deletion, or audience change.

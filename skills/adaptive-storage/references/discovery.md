# Discover and select storage

Inspect the current host's tools and environment, not a fixed engine list. Tool schemas, actual read results, and current official documentation take precedence over recollection. Search deferred tools if supported; plugin installation lists alone are insufficient evidence.

Build a lightweight session inventory with engine identity, exact account/workspace/root where known, evidence, and capability states: supported, unsupported, or unknown. Use unknown instead of guessing.

| Dimension | Questions to resolve |
| --- | --- |
| Access | Can this session list, retrieve full records, create, update, append, and read back? Is the chosen scope authorized? |
| Persistence | Durable user/project storage, temporary execution space, native retained conversation, or lossy memory? |
| Fidelity | Full text, metadata, IDs, relationships, original bytes, MIME types, file sizes, native formats? |
| Change detection | Revisions, content hashes, modified-since listing, pagination, deletion markers? |
| Concurrency | Conditional updates, exclusive creation, transactions, branch isolation, or only unconditional replacement? |
| Sharing | Which agents/devices can access it? Is this demonstrated, configured, or unknown? |
| Performance | Call overhead, batch operations, query/filter support, change-only retrieval, local cache? |
| Limits | Quotas, binary/size limits, rate limits, credentials, required runtime? |

Do not write test records to establish access unless specifically authorized. Prefer metadata and harmless scoped reads. Record latency from ordinary operations when available; do not benchmark entire stores during startup.

## Selection order

1. Apply explicit user instructions, established routes, host access constraints, scope, and audience requirements.
2. Exclude arrangements that cannot preserve required content or meet the workflow's durability/preservation requirements. Unknown critical capabilities require verification or a disclosed limitation before selection.
3. Evaluate completeness, recovery, concurrency needs, and cross-agent reach.
4. Among suitable arrangements, minimize repeated remote operations and unnecessary copies. Prefer local working storage for repeated editing when it is authorized and suitable.
5. Present meaningful alternatives when there is no accepted policy. Reuse a saved policy; do not reroute on each latency fluctuation.

Choose per role and content type. A note store need not also be a binary artifact store. A task service need not carry every research draft. A Git checkout may provide local speed and history while a remote provides sharing. Plugin count is not a ranking rule.

## Revalidation

Cache the selection and inventory evidence in the permitted policy/ledger; refresh only relevant capabilities on new sessions, credential/access changes, tool refresh, or a failed operation. Availability failure preserves pending work and the selected canonical destination. If a user has approved a fallback, use it within its exact scope and report the change; otherwise offer alternatives. Do not treat fallback use as migration or deletion authorization.

For an unfamiliar engine, bind semantic operations to observed tool schemas. Do not invent endpoints, reuse inaccessible connector credentials, or assume a script can call tools owned by another plugin. Supported basic read/write does not establish reliable multi-record sync.

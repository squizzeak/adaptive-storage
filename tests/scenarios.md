# Behavioral acceptance scenarios

These are independent agent evaluation prompts, not automated assertions about
model behavior. Use fictional records and isolated tools; do not mutate live user
stores. Record host/version, available capabilities, observed action trace, result,
and limitations. Structural CI does not imply these scenarios passed.

| Scenario | Input and capability fixture | Observable acceptance |
| --- | --- | --- |
| First use | “Use storage-init.” Durable local files, full note connector, Git with an existing private remote; no saved policy | Inspect capabilities, explain arrangements, recommend, ask choice, no premature remote writes |
| Existing policy | Same prompt with accepted global routes and bound project | Review existing policy; do not reset or request all preferences again |
| Automatic entry | Global bootstrap active, “Resume this project's research” | Load workflow, resolve policy, refresh scoped records; initialize only if genuinely unconfigured |
| Missing global locator | Policy locator is known but inaccessible | Treat policy as unavailable, not first use; do not establish a replacement global authority silently |
| Multiple engines | Task connector supports status; note connector text only; file service supports PDF | Configure per-type routes; do not choose by plugin count |
| Unsupported file | User requests editable slides; selected note engine stores text only | Suggest native/file alternatives; preserve actual artifact; no summary-as-file claim |
| Project override | Global tasks engine A, project tasks engine B; notes inherited; artifact replicas explicitly empty | Use B for tasks, inherited note route, no extra replicas |
| No shell | Cloud host exposes full remote records but no filesystem/CLI | Operate through available tools; do not require Python/Git/local files |
| Temporary files | Host files expire with session; remote slow | Disclose draft lifetime and offer earlier durable checkpoints |
| Conflict | Base text A, local B, remote C | Preserve alternatives and reconcile; no unconditional stale overwrite |
| Timeout | Create returned timeout but lookup finds same stable record | Verify existing record; do not issue duplicate create |
| Partial publication | Note saved; artifact upload failed | Record note receipt, keep artifact pending, do not mark dependent task complete |
| Git divergence | Local edits; remote changed; unrelated staged file | Preserve both; stage exact scope; no reset/clean/force-push or unrelated commit |
| PR policy | Push feature branch succeeded; canonical branch requires review | Report submitted, not canonical publication complete |
| Plugin suggestions | Required binary capability missing; host exposes plugin search | Search by capability, explain candidates; no unrequested installation or migration |
| No discovery tool | No plugin/MCP search available | Explain available alternatives; do not invent tool calls |
| Immutable/no-save | Journal workflow prohibits persistence until explicit close | No background local draft; separately identified corrections after authorized close |
| Host interruption | Local changes exist after session ends; no scheduled execution | Recover from actual durable state; do not claim work continued in background |
| New provider | Unknown connector exposes full read/create/readback but no revisions | Bind known operations; disclose weak concurrency; no invented APIs |
| Scope isolation | Connector exposes multiple projects and account-wide search | Retrieve only authorized project scope; no broad scan or transfer |

## Package and installation acceptance

Install from a clean copy using each documented path. Confirm both siblings are
available and storage-init can load adaptive-storage references. For marketplaces,
confirm component paths remain inside the installed bundle. Start a fresh session,
invoke explicit setup, then test automatic bootstrap behavior separately. Do not
record marketplace directory approval based on a local install.

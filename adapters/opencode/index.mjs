import { access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const skillsDirectory = fileURLToPath(new URL('../../skills/', import.meta.url));
const marker = '[adaptive-storage:opencode]';
const routing = `${marker}
For work that uses persistent project context, task tracking, notes, or artifacts,
load the adaptive-storage skill using the skill tool before relying on stored context.
Run its session preflight: reuse accepted global/project policy, inspect pending work,
and refresh only relevant context. If no applicable accepted policy exists, follow
its first-use setup and ask the user to select among available storage arrangements.
Before reporting the applicable unit of work complete, follow its configured
publication and verification policy. Respect explicit checkpoint, no-save, and
end-only workflows; do not publish merely because a turn or session is idle.
Skip this workflow for disposable questions. If skill access is denied or unavailable,
report the limitation for dependent storage work; do not bypass host permissions.
This adapter supplies routing instructions, not storage authorization or a sync service.`;
const compaction = `${marker}
When summarizing this session, retain any already-established storage policy locator,
workspace identity, accepted project overrides, last verified freshness, pending
publication/conflict state, and the user's saving boundaries. Do not invent missing
state or copy credentials. On continuation, load adaptive-storage and resume its
preflight before dependent storage work. Compaction does not authorize publication.`;

/** Optional OpenCode plugin. No writes, network requests, or model calls. */
export default async function AdaptiveStoragePlugin(_input, options = {}) {
  const automatic = options.automatic ?? true;
  const commandName = options.commandName ?? 'storage-init';
  if (typeof automatic !== 'boolean') {
    throw new TypeError('Adaptive Storage: automatic must be a boolean');
  }
  if (typeof commandName !== 'string' || !/^[a-z][a-z0-9-]{0,63}$/.test(commandName)) {
    throw new TypeError('Adaptive Storage: commandName must be a lowercase command name');
  }
  // Catch partial installs before adding a command that could not load its policy.
  for (const relative of [
    '../../skills/storage-init/SKILL.md',
    '../../skills/adaptive-storage/SKILL.md',
    '../../skills/adaptive-storage/references/setup.md',
  ]) {
    try {
      await access(new URL(relative, import.meta.url));
    } catch (cause) {
      throw new Error('Adaptive Storage: incomplete package; retain adapters/ and both skills/ folders together', { cause });
    }
  }

  return {
    async config(config) {
      config.skills ??= {};
      config.skills.paths ??= [];
      if (!config.skills.paths.includes(skillsDirectory)) {
        config.skills.paths.push(skillsDirectory);
      }
      config.command ??= {};
      // User/project commands win. commandName can explicitly avoid a collision.
      if (!Object.hasOwn(config.command, commandName)) {
        config.command[commandName] = {
          description: 'Choose storage engines and configure global or project storage',
          template: 'Load the storage-init skill with the skill tool and follow its setup/review workflow. '
            + 'Reuse accepted preferences; do not reset configuration or migrate records. '
            + 'Discover the capabilities available in this session and explain options before establishing new routes.\n\n'
            + 'User request: $ARGUMENTS',
        };
      }
    },
    async 'experimental.chat.system.transform'(input, output) {
      // Excludes calls without a session; title/summary calls may still have one.
      if (automatic && input.sessionID && !output.system.some(text => text.includes(marker))) {
        output.system.push(routing);
      }
    },
    async 'experimental.session.compacting'(_input, output) {
      if (automatic && !output.context.some(text => text.includes(marker))) {
        output.context.push(compaction);
      }
    },
  };
}

import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtemp, mkdir, cp, rm, realpath } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import plugin from '../adapters/opencode/index.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const skills = fileURLToPath(new URL('../skills/', import.meta.url));

// No SDK calls are permitted, even during initialization or hook execution.
const context = new Proxy({}, { get() { throw new Error('Unexpected host side effect'); } });

test('registers command and discoverable skill path without losing config', async () => {
  const hooks = await plugin(context);
  const existingCommand = { template: 'test', description: 'existing' };
  const config = { command: { test: existingCommand }, skills: { paths: ['/other'], urls: ['https://example.test/skills'] }, permission: { skill: 'ask' } };
  await hooks.config(config);
  await hooks.config(config);
  assert.deepEqual(config.skills.paths, ['/other', skills]);
  assert.deepEqual(config.skills.urls, ['https://example.test/skills']);
  assert.equal(config.command.test, existingCommand);
  assert.match(config.command['storage-init'].template, /\$ARGUMENTS/);
  assert.match(config.command['storage-init'].template, /storage-init skill/);
  assert.deepEqual(config.permission, { skill: 'ask' });
});

test('preserves colliding commands, including an explicitly disabled entry', async () => {
  const hooks = await plugin(context);
  for (const value of [{ template: 'mine' }, null]) {
    const config = { command: { 'storage-init': value } };
    await hooks.config(config);
    assert.equal(config.command['storage-init'], value);
  }
  const alias = await plugin(context, { commandName: 'adaptive-storage-init' });
  const config = { command: { 'storage-init': { template: 'mine' } } };
  await alias.config(config);
  assert.equal(config.command['storage-init'].template, 'mine');
  assert.ok(config.command['adaptive-storage-init']);
});

test('appends routing once without changing existing system instructions', async () => {
  const hooks = await plugin(context);
  const output = { system: ['existing system instructions'] };
  await hooks['experimental.chat.system.transform']({ sessionID: 'one' }, output);
  await hooks['experimental.chat.system.transform']({ sessionID: 'one' }, output);
  assert.equal(output.system.length, 2);
  assert.equal(output.system[0], 'existing system instructions');
  assert.match(output.system[1], /no-save/);
  assert.match(output.system[1], /Skip this workflow for disposable questions/);
  const other = { system: [] };
  await hooks['experimental.chat.system.transform']({ sessionID: 'two' }, other);
  assert.equal(other.system.length, 1);
});

test('does not inject into auxiliary model calls without a session', async () => {
  const hooks = await plugin(context);
  const output = { system: ['title instructions'] };
  await hooks['experimental.chat.system.transform']({}, output);
  assert.deepEqual(output.system, ['title instructions']);
});

test('compaction retains boundaries without replacing host prompt', async () => {
  const hooks = await plugin(context);
  const output = { context: ['existing'], prompt: 'custom compaction prompt' };
  await hooks['experimental.session.compacting']({ sessionID: 'one' }, output);
  await hooks['experimental.session.compacting']({ sessionID: 'one' }, output);
  assert.equal(output.context.length, 2);
  assert.equal(output.context[0], 'existing');
  assert.equal(output.prompt, 'custom compaction prompt');
  assert.match(output.context[1], /does not authorize publication/);
});

test('explicit-only option retains setup command and disables automatic injection', async () => {
  const hooks = await plugin(context, { automatic: false });
  const system = { system: [] }, compact = { context: [] }, config = {};
  await hooks.config(config);
  await hooks['experimental.chat.system.transform']({ sessionID: 'one' }, system);
  await hooks['experimental.session.compacting']({ sessionID: 'one' }, compact);
  assert.deepEqual(system.system, []);
  assert.deepEqual(compact.context, []);
  assert.ok(config.command['storage-init']);
});

test('exposes no idle/event, remote-write, permission, or autonomous prompt hooks', async () => {
  const hooks = await plugin(context);
  assert.deepEqual(Object.keys(hooks).sort(), ['config', 'experimental.chat.system.transform', 'experimental.session.compacting'].sort());
});

test('rejects invalid options before registering routes', async () => {
  await assert.rejects(plugin(context, { automatic: 'false' }), /boolean/);
  await assert.rejects(plugin(context, { commandName: '../bad' }), /command name/);
});

test('relocated complete package works; partial adapter-only install fails clearly', async () => {
  const temp = await mkdtemp(join(tmpdir(), 'adaptive-storage-test-'));
  try {
    await mkdir(join(temp, 'adapters/opencode'), { recursive: true });
    await cp(join(root, 'adapters/opencode/index.mjs'), join(temp, 'adapters/opencode/index.mjs'));
    const relocated = (await import(pathToFileURL(join(temp, 'adapters/opencode/index.mjs')).href)).default;
    await assert.rejects(relocated(context), /incomplete package/);
    await cp(join(root, 'skills'), join(temp, 'skills'), { recursive: true });
    const hooks = await relocated(context);
    const config = {};
    await hooks.config(config);
    assert.equal(await realpath(config.skills.paths[0]), await realpath(join(temp, 'skills')));
  } finally {
    await rm(temp, { recursive: true, force: true });
  }
});

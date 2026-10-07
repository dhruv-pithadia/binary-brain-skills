import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { z } from 'zod';
import { RedisStore } from 'rate-limit-redis';

const text = readFileSync('skills/security-and-hardening/references/auth-and-input.md', 'utf8');
const snippet = text.match(/```typescript\n([\s\S]*?)```/)[1].replace("import { z } from 'zod';", '');
const { Registration, TaskPatch } = new Function('z', snippet + '\nreturn { Registration, TaskPatch };')(z);

test('documented registration and update schemas reject privilege injection', () => {
  const valid = { email: 'user@example.com', password: 'long-valid-passphrase' };
  assert.equal(Registration.safeParse(valid).success, true);
  assert.equal(Registration.safeParse({ ...valid, role: 'admin' }).success, false);
  for (const field of ['ownerId', 'tenantId', 'role']) {
    assert.equal(TaskPatch.safeParse({ [field]: 'injected' }).success, false);
  }
  assert.equal(TaskPatch.safeParse({}).success, false);
  assert.deepEqual(TaskPatch.parse({ completed: false }), { completed: false });
});
test('current RedisStore accepts the documented adapter with isolated limiter prefixes', () => {
  // Constructor compatibility only; a live Redis connection is not exercised.
  const auth = new RedisStore({ sendCommand: async () => '', prefix: 'rl:auth:' });
  const api = new RedisStore({ sendCommand: async () => '', prefix: 'rl:api:' });
  assert.notEqual(auth.prefix, api.prefix);
});

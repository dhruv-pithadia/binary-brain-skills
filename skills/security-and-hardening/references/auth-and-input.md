# Authentication and input patterns

Adapt to installed versions and product policy. These examples address privilege injection and mass assignment; they do not replace the application's session, CSRF, transaction, or error-handling layers.

## Public registration and field-restricted updates

Node/Zod example (uses APIs shared by Zod 3 and 4):

```typescript
import { z } from 'zod';

const Registration = z.object({
  email: z.string().trim().toLowerCase().email(),
  password: z.string().min(12).max(128),
}).strict();

const TaskPatch = z.object({
  title: z.string().trim().min(1).max(200).optional(),
  completed: z.boolean().optional(),
}).strict().refine(value => Object.keys(value).length > 0, 'Empty update');
```

Set `role: 'user'` server-side from `Registration` data. A separate role-management operation must verify the actor's administrative permission and which roles they can grant; a valid enum is not that permission.

For task updates, validate `TaskPatch` and pass **only** its parsed fields into an ownership/tenant-scoped atomic update. Do not pass `req.body` into an ORM after checking ownership. Scope the write itself, not just a preceding read, so concurrent ownership changes cannot bypass the check:

```typescript
const parsed = TaskPatch.safeParse(req.body);
if (!parsed.success) return res.status(422).json({ error: 'Invalid task update' });
// Adapt this Prisma-style call to the installed ORM and tenant model.
const result = await db.task.updateMany({
  where: { id: req.params.id, ownerId: req.user.id, tenantId: req.user.tenantId },
  data: parsed.data,
});
if (result.count === 0) return res.status(404).json({ error: 'Not found' });
return res.sendStatus(204);
```

Test `ownerId`, `tenantId`, and role injection, another actor's task, an empty patch, and a valid update. Expose only approved response fields.

Pydantic v2 boundary schemas also forbid unknown fields:

```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None
```

Use `body.model_dump(exclude_unset=True)` and reject empty patches or explicit nulls for non-nullable fields before a scoped update. `model_dump()` without `exclude_unset` can overwrite omitted fields with defaults. Choose password length according to the product's authentication policy, not this illustrative schema alone.

## Password storage

Prefer a maintained Argon2id implementation. OWASP's current baseline is memory >=19 MiB, time cost >=2, parallelism 1; benchmark production concurrency and increase costs when feasible. Library defaults can differ, so inspect rather than assume. Store the encoded algorithm/parameters/salt/hash and rehash on successful login when policy changes.

For legacy bcrypt, use a benchmarked work factor at least 10. Enforce the 72-byte UTF-8 limit on new passwords **before hashing**; `string.length` and Python `len(str)` do not measure bytes. Do not silently trim, truncate, or introduce an ad hoc prehash that breaks verification or creates new weaknesses. Preserve existing verification semantics during migration and move users to Argon2id safely. Bound overall request size to prevent expensive hashing abuse, and rate-limit auth attempts without disclosing account existence.

## Redis rate-limiter integration

Current `rate-limit-redis` exposes a named `RedisStore` and a `sendCommand` adapter. Use a connected `node-redis` client. Create a separate store and prefix for each limiter:

```typescript
import { rateLimit } from 'express-rate-limit';
import { RedisStore } from 'rate-limit-redis';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 10,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redis.sendCommand(args),
    prefix: 'rl:auth:',
  }),
});
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 100,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redis.sendCommand(args),
    prefix: 'rl:api:',
  }),
});
app.use('/api/auth', authLimiter);
app.use('/api', apiLimiter);
```

This intentionally applies both budgets to auth requests; choose routing explicitly if budgets should be exclusive. Validate proxy trust and IPv6 key behavior with the installed `express-rate-limit` version. Distributed counters need shared Redis and a defined outage policy; decide fail-open versus fail-closed from availability and abuse risk.

Sources: [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [Zod object schemas](https://zod.dev/api#objects), [Pydantic model configuration](https://docs.pydantic.dev/latest/concepts/config/), [RedisStore adapter and prefixes](https://github.com/express-rate-limit/rate-limit-redis).

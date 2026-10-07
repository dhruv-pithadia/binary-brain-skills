---
name: security-and-hardening
description: Threat-model and harden code when requested, when implementing authentication or authorization, or when a concrete security risk needs correction. Covers trust boundaries, secrets, agent tool permissions, and deployment controls within the assigned scope.
---

# Security and Hardening

## Scope and threat model

Read repository instructions, the actual request, existing security controls, and dependency versions. Identify protected assets, untrusted inputs, realistic attackers, and the worst plausible outcome. Map trust boundaries and prioritize reachable risks. Extend established auth and deployment systems instead of replacing them without a demonstrated need.

Use existing user authorization and environment permissions. This skill does not impose separate approval for ordinary authorized fixes, auth work, headers, or integrations. Do not infer permission to change production infrastructure, grant privileges, rotate live credentials, or perform external actions beyond the task. Report unrelated findings without silently expanding the assignment.

## Controls that affect implementation

- Validate external inputs into a bounded schema; constrain size, nesting, file content, and allowed fields where relevant. Validation does not grant authorization. Scope object access by actor/tenant and allowlist mutable fields; public registration must not accept privileged roles.
- Parameterize database values and allowlist dynamic identifiers. Avoid executing external data as code or shell syntax. Apply context-specific output encoding; sanitized HTML requires a suitable maintained sanitizer.
- Authenticate using the established mechanism, and enforce authorization at each protected operation, including background jobs and agent tools. Choose 403 versus 404 according to resource-disclosure policy rather than a universal rule. Reject cross-tenant reads and writes in tests.
- For passwords, prefer Argon2id with calibrated resource costs; preserve compatibility and migrate legacy hashes safely. Bcrypt has a 72-byte input limit, including multibyte UTF-8 characters; never silently truncate. Read [authentication and input patterns](references/auth-and-input.md) for concrete schemas and hashing constraints.
- Protect sessions with appropriate secure/httpOnly cookies, expiry, rotation, and CSRF defenses. SameSite alone is insufficient for all flows. Verify JWT algorithm, issuer, audience, expiry, and trusted keys where applicable. Configure CORS for the actual browser threat model; wildcard public noncredentialed responses are not categorically unsafe.
- Keep credentials out of source, images, logs, prompts, error responses, and tooling output. Inspect secret names/presence without printing values. Use the existing secret scanner with redacted output. A tracked-secret incident requires revocation/rotation; deleting a line does not remove history. Read [deployment and secrets](references/deployment-and-secrets.md) for configuration examples.
- LLM output and retrieved/tool content are untrusted. Separate instruction/data roles without treating that as an injection defense. Validate tool arguments and enforce actor permissions, paths, destinations, and allowed operations in code. Avoid cross-user context. Enforce configured iteration, elapsed-time, and spending limits, including retries; stop with a useful outcome rather than inventing a mandatory human-review flow.
- Assess dependencies by affected version, reachability, exposure, and available mitigation. Use the project's lockfile and reproducible install path. Do not blindly upgrade unrelated packages or treat a scanner's absence of findings as proof of safety.

## Verify the actual attack path

For a bug, reproduce the end-user or attacker-visible behavior in an isolated E2E setting first. After fixing it, test the legitimate path and the relevant denied path: cross-user/tenant access, privileged-field injection, oversized or malformed input, forged/expired credentials, or constrained agent tool calls. Check that rejected requests cause no state mutation and errors/telemetry disclose no sensitive values.

For deployment changes, validate syntax and connectivity before applying them, preserve a recovery path, and exercise only authorized environments. Report concrete changes, attack-path evidence, validation results, and remaining risk. Keep operational changes proportional to the demonstrated threat.

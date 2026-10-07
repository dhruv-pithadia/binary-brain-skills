# Deployment, secrets, and supply chain

Apply these patterns only to the requested deployment and installed software versions. Preserve remote recovery access before changing SSH/firewall settings. Validate configuration before reload, and do not execute example infrastructure mutations automatically.

## Secret storage

Commit only placeholder `.env.example` values. Exclude the project's actual secret-bearing files from Git, build contexts, artifacts, and backups where appropriate. A blanket `*.key` exclusion is not a substitute for classifying the real files. Use a secret manager or workload identity when available. Protected environment files can be acceptable when the deployment requires them: restrict ownership, mode, mount visibility, and rotation. Environment variables can still leak through process access, crash dumps, diagnostic output, or inherited child processes.

For a system service, a root-owned `0600` environment file can be read by the systemd manager and passed to a non-root service. It is not necessary to make the file world/group readable for the service user. Prefer systemd credentials when supported by the service; check the deployment's threat model and version. Do not embed production values in PM2 or other source-controlled configuration.

Validate required variables by **name**, never log their values. Configure secret scanning to redact findings; do not pipe a raw staged diff through a secret regex that prints the matches. If a real key was exposed, follow the provider's rotation/revocation process and the repository's history-remediation policy.

## Nginx rate limiting

`limit_req_zone` belongs in the `http` context; `limit_req` can appear in `http`, `server`, or `location`. This is a rate-limiting fragment for an existing HTTP configuration, not a complete TLS deployment:

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    server {
        listen 80;
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
            proxy_pass http://127.0.0.1:3000;
        }
    }
}
```

Keep the deployment's existing TLS termination and HTTPS redirects; do not replace them with this example. If behind a proxy, configure trusted real-IP sources explicitly before using client-IP keys. Test with `nginx -t`, then verify limits and legitimate traffic in the authorized environment. Select CSP and frame policy from actual frontend requirements. Enable HSTS `includeSubDomains` or preload only when every affected domain can meet the HTTPS commitment.

## Reproducible Python dependencies

For a project already using pip-tools and requirements files:

```bash
pip-compile --generate-hashes --output-file requirements.txt requirements.in
pip install --require-hashes -r requirements.txt
```

Review generated dependency changes; do not manually edit a generated lockfile. Hash-checking requires pinned, hashed transitive dependencies and compatible distributions, and is not equivalent to vulnerability scanning. Use the project's existing environment manager when it has a different locking workflow. Match target Python/platform and separately account for build dependencies.

Use the established dependency scanner and triage actual reachability/exposure. For Node use the committed lockfile and the package manager's frozen install mode; for Rust retain `Cargo.lock` where the project requires it. Do not introduce third-party audit tools or arbitrary severity deadlines without a demonstrated project need.

Sources: [Nginx limit directives](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html), [pip-compile flags](https://pip-tools.readthedocs.io/en/stable/reference/pip-compile/), [pip hash checking](https://pip.pypa.io/en/stable/topics/secure-installs/), [systemd execution environment and credentials](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html).

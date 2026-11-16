# Security Policy

## Scope

Siren-Trap is a defensive research prototype. Security reports concerning this repository, its dependencies, or unsafe defaults are welcome.

## Reporting

Do not publish exploitable details in a public issue. Contact the repository maintainers through the private security reporting mechanism available on the GitHub repository. Include affected version/commit, impact, reproduction steps, and a suggested mitigation where possible.

## Supported versions

Only the latest development branch is currently supported. There are no stable releases yet.

## Operational guidance

- Keep the service bound to localhost unless a deployment has been separately reviewed.
- Do not use real third-party agents without explicit authorization.
- Do not submit secrets, credentials, personal data, or raw microphone recordings.
- Treat observations as untrusted input and never execute them.
- Review dependency licenses, provenance, maintenance activity, and known vulnerabilities before upgrading.

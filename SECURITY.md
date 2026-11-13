# Security

## Supported versions

| Version | Status |
|---|---|
| 0.1.x | The only published line. In active development. Fixes land on `main` and are noted in [CHANGELOG.md](CHANGELOG.md). |

There is no older release branch.

## Reporting a vulnerability

Report vulnerabilities in this repository through GitHub private vulnerability reporting:

<https://github.com/ogooluwanick/feature-guardian/security/advisories/new>

That opens a private draft security advisory for the maintainer, [@ogooluwanick](https://github.com/ogooluwanick).

You can also report privately by email to ogooluwanick@gmail.com. GitHub private vulnerability reporting and that address are the two private channels. Use one of them.

Please include:

- the Feature Guardian version and schema (0.1.0 / 0.1 in the current release)
- the files or scripts involved
- what you observed and the impact
- steps to reproduce

Do not include secrets, tokens, passwords, or credential-bearing connection strings. Describe them as names only.

Do not open a public GitHub issue, discussion, or pull request for an unfixed vulnerability.

If the advisory link says private vulnerability reporting is turned off, email ogooluwanick@gmail.com. Enabling that page is GitHub's "Private vulnerability reporting" setting on the repository. It is not turned on by this file alone.

The maintainer will reply on the channel you used. This project does not publish a response-time guarantee.

## Scope

In scope: `SKILL.md`, `references/`, templates, and `scripts/bootstrap_memory.py` and `scripts/validate_memory.py`, where a flaw in this repository can corrupt or wipe Feature Guardian memory, hide an invalid memory file, or instruct an agent to store secrets.

`bootstrap_memory.py --force` overwrites `PRODUCT.md` on purpose. That flag is documented behavior, not a vulnerability by itself.

Out of scope for advisories on this repository: bugs in an application that merely uses Feature Guardian. That application's memory lives in its own `.feature-guardian/` directory. Report those issues to that project's maintainers.

## What this project stores

v0.1 has no hosted service, account system, telemetry, or cloud sync. Memory files are plain Markdown in the user's repository. The skill's rule is to record configuration names only, never secret values.

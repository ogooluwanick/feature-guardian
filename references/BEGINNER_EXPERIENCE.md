# Beginner Experience

Feature Guardian should be invisible to casual users.

## Normal interaction

User: **"Add Google login."**

Guardian internally:

```text
identify feature → load memory → inspect auth code
→ assess risk → implement → run relevant tests
→ update memory → report concise result
```

No manual `/update-feature` or `/save-history` commands.

## Friendly warnings

Translate technical risk:

| Avoid | Prefer |
|---|---|
| Migration required | This changes the database structure. I'll inspect the migration and avoid destructive changes unless you explicitly need them. |
| Contract changed | This API response is used elsewhere. Changing it may break related features, so they need review and tests. |

Keep advanced detail available in memory, not overwhelming in chat.

## Final user report

Compact checkpoint after meaningful work:

```text
✓ Authentication update completed

Changed
- Added Google OAuth provider configuration.

Verification
- 12 relevant tests passed.
- Build passed.

Feature health
HEALTHY — MEDIUM confidence

Remaining
- Google sandbox login not observed in staging.
```

Do not dump full feature memory unless requested.

## Inspecting status

- Read `.feature-guardian/PRODUCT.md` for product overview and registry.
- Open `.feature-guardian/features/<slug>.md` for feature detail.
- Run validator: `python path/to/validate_memory.py .`

## First-time setup

1. Install skill + Cursor rule (see README).
2. Run bootstrap in project root.
3. Ask the agent to work normally; memory populates over time.

## Uninstall

1. Remove `.cursor/rules/feature-guardian.mdc` (or project equivalent).
2. Remove installed skill directory.
3. Optionally keep `.feature-guardian/` as project documentation or delete after backup if no longer wanted.

Uninstalling the skill does not delete memory unless you choose to.

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
- Run the validator from the installed skill: `python3 path/to/feature-guardian/scripts/validate_memory.py .`

## First-time setup

1. Install the skill and the Cursor rule (see [README.md](../README.md) and [adapters/cursor/INSTALL.md](../adapters/cursor/INSTALL.md)).
2. Run `bootstrap_memory.py` in the project root.
3. Ask the agent to work normally; memory populates over time.

## Uninstall

1. Remove `.cursor/rules/feature-guardian.mdc`.
2. Remove the installed skill directory (`.cursor/skills/feature-guardian/` or `.agents/skills/feature-guardian/`).
3. Keep `.feature-guardian/` when the project should retain the history. Delete that directory only when the memory is no longer wanted.

Uninstalling the skill does not delete memory unless you choose to.

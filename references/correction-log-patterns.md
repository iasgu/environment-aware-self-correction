# Correction Log Patterns

Use this reference when a user points out repeated mistakes or an environment-specific failure should become a durable rule.

## Minimal Entry

```text
CONTEXT: Windows PowerShell command execution in a project with Chinese filenames
REFLECTION: I assumed Bash syntax and used a heredoc, which PowerShell cannot parse.
LESSON: Detect the shell first. In PowerShell, use here-strings piped to Python and keep inline Python source ASCII-only when encoding is uncertain.
```

## Where To Record

- Project-specific rule: write a short project doc such as `docs/local-environment.md`.
- Agent-wide rule: write to local correction memory if available.
- Temporary one-off issue: mention it in the final answer, but do not create permanent memory.

## What Not To Record

- API keys, tokens, passwords, cookies, `.env` values, or private account details.
- Guesses that were not verified.
- One-time instructions that are not likely to recur.

## Good Correction Categories

- Shell syntax mismatch.
- Encoding or locale mismatch.
- Non-ASCII path handling.
- Sandbox or escalation behavior.
- Service startup timing.
- Git/GitHub publishing assumptions.
- Test commands that write outside the workspace.

---
name: environment-aware-self-correction
description: Probe and adapt to the local execution environment before acting, then turn user corrections and repeated command failures into durable operating rules. Use when Codex is corrected by the user, repeatedly fails on shell syntax, encoding, paths, services, Git/GitHub publishing, Windows PowerShell, UTF-8/GBK issues, Chinese filenames, sandbox/escalation behavior, or any task where local environment assumptions can break the work.
---

# Environment-Aware Self Correction

Use this skill to stop repeating environment-specific mistakes. The goal is to pause, inspect, adapt, verify, and record a reusable lesson before continuing.

## Core Workflow

1. Acknowledge the correction without arguing.
2. Stop the risky action if the same error could repeat.
3. Probe the local environment before making more assumptions.
4. Choose commands and file operations that match the detected shell, encoding, sandbox, path style, and services.
5. Verify with a small, reversible check before doing the full operation.
6. Record the lesson in the project or local correction memory when the mistake is likely to recur.

## Environment Probe

Run the bundled probe when the local environment is unclear:

```powershell
python skills/environment-aware-self-correction/scripts/probe_environment.py --project-root .
```

Read only the fields relevant to the task. Do not print secrets. If `.env` is involved, inspect key names or configuration presence, not secret values.

Probe at least these areas before fragile work:

- Shell: PowerShell, Bash, cmd, WSL, or another shell.
- Encoding: console/code page, Python stdin/stdout, preferred locale, file encodings.
- Paths: workspace path, non-ASCII filenames, spaces, Windows vs POSIX separators.
- Services: local ports, Docker containers, dev servers, browser processes.
- Tooling: Python, Node, Git, GitHub CLI, Docker, package managers.
- Sandbox: whether reading, writing, networking, GUI launch, or publishing requires escalation.

## Command Selection Rules

- Match syntax to the actual shell. Do not use Bash heredoc in Windows PowerShell.
- In Windows PowerShell, prefer:

```powershell
@'
print("ASCII-only inline Python source")
'@ | python -
```

- Keep piped inline Python source ASCII-only when console input encoding is uncertain. For Chinese text, read from UTF-8 files or use Unicode escapes.
- Use explicit encodings in Python:

```python
path.read_text(encoding="utf-8")
csv_path.open("r", encoding="utf-8-sig", newline="")
json.dumps(data, ensure_ascii=False)
```

- Use `-LiteralPath` in PowerShell and `pathlib.Path` in Python for paths with spaces, Chinese characters, or wildcard-like characters.
- Do not enumerate paths in one shell and delete or move them in another.
- Do not change console encoding unless a test proves it improves this client. A forced UTF-8 console can make captured output worse on some Windows setups.

For Windows-specific details, read `references/windows-powershell-encoding.md`.

## Correction Recording

Record a correction when one of these is true:

- The user explicitly says the same class of mistake keeps happening.
- A command fails because of shell syntax, encoding, sandbox, network, or path assumptions.
- A fix changes the way future commands should be written.
- A local project has non-obvious service, encoding, or file layout rules.

Use this shape:

```text
CONTEXT: where the mistake occurred
REFLECTION: what assumption failed
LESSON: what to do differently next time
```

Prefer project-local documentation for project-specific rules. Prefer local agent memory for broad rules that apply across sessions. Never store credentials, personal secrets, or raw `.env` contents.

For logging patterns, read `references/correction-log-patterns.md`.

## Publishing And GitHub

Before publishing a skill:

- Check whether the current directory is a Git repository.
- Check whether `gh` exists; if not, publishing needs a destination Git remote or another approved GitHub method.
- Avoid committing unrelated dirty files.
- Validate the skill with the creator validation script when available.
- If network access or GUI/browser launch is required, request escalation rather than improvising around the sandbox.

## Verification

After adapting to the environment, verify the smallest meaningful thing:

- Compile or syntax-check changed code.
- Hit a local health endpoint.
- Confirm a service port is listening.
- Run the probe script and confirm expected fields.
- Validate the skill frontmatter and required files.

If verification fails, update the correction note with the new failure mode before continuing.

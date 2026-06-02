# Windows PowerShell And Encoding Guardrails

Use this reference when working on Windows, especially with PowerShell 5.1, Chinese filenames, UTF-8 files, GBK/cp936 locales, or piped Python snippets.

## Common Failure Pattern

Windows PowerShell is not Bash. These fail in PowerShell:

```powershell
python - <<'PY'
print("hello")
PY
```

Use this instead:

```powershell
@'
print("hello")
'@ | python -
```

## Chinese Text In Inline Python

Avoid direct Chinese characters in piped inline Python when the input encoding is uncertain. They may become `?` before Python receives them.

Safer options:

```powershell
@'
text = "\u6d59\u6c5f\u7701"
print(text)
'@ | python -
```

Or read Chinese from a file with explicit encoding:

```python
from pathlib import Path
text = Path("frontend/app.js").read_text(encoding="utf-8")
```

## File Encoding Defaults

Prefer explicit encodings:

```python
Path("file.txt").read_text(encoding="utf-8")
Path("manifest.csv").open("r", encoding="utf-8-sig", newline="")
Path("out.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
```

Use `utf-8-sig` for CSV files that may have a BOM.

## PowerShell Path Rules

Use `-LiteralPath` when paths may contain Chinese characters, spaces, brackets, wildcard characters, or punctuation:

```powershell
Get-Content -LiteralPath "downloads\industry\manifest_all.csv" -Encoding UTF8
Remove-Item -LiteralPath $path -Force
Move-Item -LiteralPath $source -Destination $target
```

Do not build destructive `cmd /c` strings from PowerShell-enumerated paths.

## Console Encoding

Do not blindly set:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

On some clients this makes captured output worse. Test first with a harmless Chinese output sample if encoding changes are necessary.

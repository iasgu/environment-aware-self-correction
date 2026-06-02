# 给中文新手的说明：为什么 AI 编程要先检查环境

这份说明写给刚开始用 AI 编程的人。目标不是让你马上变成命令行专家，而是让你能看懂 AI 为什么会在“中文路径、UTF-8、PowerShell”这些地方翻车，以及怎么让它少翻车。

## 1. AI 为什么会写错命令

AI 看到“运行一个 Python 脚本”，脑子里可能会默认你在 Linux 或 macOS 上，于是写出这种命令：

```bash
python - <<'PY'
print("hello")
PY
```

这在 Bash 里可以，但在 Windows PowerShell 里不行。PowerShell 需要这样写：

```powershell
@'
print("hello")
'@ | python -
```

所以第一条规则是：先确认 shell 是什么，再写命令。

## 2. 什么是 shell

shell 就是你输入命令的地方。常见的有：

- PowerShell：Windows 上很常见。
- cmd：老式 Windows 命令行。
- Bash：Linux、macOS、Git Bash、WSL 常见。

它们看起来都是“黑框框”，但语法不一样。AI 如果搞错 shell，就像拿错钥匙开门。

## 3. 中文路径为什么容易出事

英文路径通常比较简单：

```text
C:\project\report.pdf
```

中文路径可能是：

```text
C:\Users\majia\Documents\report-download\downloads\industry\01_环境影响评价\建设项目环境影响报告表\正文\某某项目.pdf
```

如果命令没有正确处理这些路径，可能会出现：

- 文件找不到。
- 通配符误匹配。
- 路径被拆开。
- 中文变成乱码。

在 PowerShell 里，处理中文路径更稳的方式是用 `-LiteralPath`：

```powershell
Get-Content -LiteralPath "中文路径\文件.txt" -Encoding UTF8
```

在 Python 里，推荐用 `pathlib.Path`。

## 4. UTF-8、GBK、cp936 是什么

你可以把编码理解成“文字和数字之间的翻译表”。

同一句中文，如果用不同编码读写，就可能变成乱码。

常见编码：

- UTF-8：现在最常用，适合跨平台。
- GBK / cp936：中文 Windows 上经常遇到。
- UTF-8 with BOM：有些 CSV 文件会带一个隐藏开头标记。

所以 AI 读文件时，不应该猜编码，而应该明确写：

```python
Path("file.txt").read_text(encoding="utf-8")
```

CSV 如果可能带 BOM，用：

```python
open("manifest.csv", "r", encoding="utf-8-sig", newline="")
```

## 5. 为什么不要随便改控制台编码

有时候看到乱码，第一反应是强行设置 UTF-8：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

但在某些 AI 工具里，这反而会让工具捕获到的输出更乱。正确做法是先用小命令测试，确认有效后再改。

这个 Skill 的默认建议是：不要盲目改控制台编码，优先在读写文件时显式指定编码。

## 6. 环境探测脚本看什么

运行：

```powershell
python skills/environment-aware-self-correction/scripts/probe_environment.py --project-root . --pretty
```

重点看：

```json
{
  "platform": {},
  "python": {},
  "project": {},
  "tools": {},
  "git": {},
  "docker": {}
}
```

你不需要理解所有字段，只要知道它们回答了这些问题：

- 我是什么系统？
- Python 是哪个？
- 默认编码是什么？
- 项目里有没有大量中文路径？
- Git、Docker、Node、GitHub CLI 在不在？
- 当前目录是不是 Git 仓库？

## 7. 怎么指挥 AI 使用这个 Skill

当你发现 AI 又开始猜环境，可以这样说：

```text
先别继续，使用 environment-aware-self-correction 探测本机环境。
```

当它重复犯错，可以这样说：

```text
把这次错误写成纠错经验：以后在 PowerShell 里不要用 Bash heredoc。
```

当你不确定为什么命令失败，可以这样说：

```text
先判断这是 shell 语法问题、编码问题、路径问题，还是服务没有启动。
```

## 8. 给初学者的最重要三句话

1. 不要让 AI 直接猜你的电脑环境。
2. 中文路径和编码问题要显式处理。
3. AI 犯过的错，要让它写成规则，下次先检查。

这就是这个 Skill 的核心价值。

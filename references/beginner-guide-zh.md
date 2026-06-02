# 给中文新手的说明：为什么 AI 编程要先检查环境

这份说明写给刚开始用 AI 编程的人。目标不是让你马上变成命令行专家，而是让你能看懂：AI 为什么会在 PowerShell、中文路径、UTF-8、Docker、GitHub 这些地方翻车，以及怎么让它少翻车。

## 1. 先记住一句话

AI 写命令前如果不看环境，就是在“闭眼开车”。

它可能不知道你现在用的是 Windows PowerShell，还是 Bash；不知道你的路径里有没有中文；不知道当前服务有没有启动；也不知道文件应该用 UTF-8 还是 GBK 读。

所以正确顺序不是：

```text
想到命令 -> 直接执行 -> 出错再猜
```

而是：

```text
先检查环境 -> 选正确写法 -> 小范围验证 -> 再正式执行
```

## 2. 什么是 Shell

Shell 就是你输入命令的地方。常见的有：

- PowerShell：Windows 上很常见。
- cmd：老式 Windows 命令行。
- Bash：Linux、macOS、Git Bash、WSL 常见。

它们看起来都像“命令行窗口”，但语法不一样。

比如这段命令在 Bash 里可以：

```bash
python - <<'PY'
print("hello")
PY
```

但在 Windows PowerShell 里不行。PowerShell 应该这样写：

```powershell
@'
print("hello")
'@ | python -
```

所以如果 AI 不先判断 Shell，很容易拿错钥匙开错门。

## 3. 中文路径为什么容易出事

英文路径通常比较简单：

```text
C:\project\report.pdf
```

中文路径可能是：

```text
C:\Users\majia\Documents\report-download\downloads\industry\01_环境影响评价\建设项目环境影响报告表\正文\某某项目.pdf
```

如果命令写法不稳，可能出现：

- 文件找不到。
- 路径被空格或特殊符号拆开。
- `*`、`[`、`]` 等字符被当成通配符。
- 中文显示成乱码。
- PowerShell 和 Python 对同一条路径理解不一致。

在 PowerShell 里处理这类路径，优先使用 `-LiteralPath`：

```powershell
Get-Content -LiteralPath "中文路径\文件.txt" -Encoding UTF8
```

在 Python 里，优先使用 `pathlib.Path`：

```python
from pathlib import Path

path = Path("中文路径") / "文件.txt"
text = path.read_text(encoding="utf-8")
```

## 4. UTF-8、GBK、cp936 是什么

你可以把编码理解成“文字和数字之间的翻译表”。

电脑底层保存的是数字。中文、英文、符号要显示出来，就需要一张翻译表。UTF-8、GBK、cp936 就是不同的翻译表。

同一段中文，如果用错翻译表读取，就会变成乱码。

常见编码：

- UTF-8：现在最常用，跨平台更稳。
- GBK / cp936：中文 Windows 上经常遇到。
- UTF-8 with BOM：一些 CSV 文件会带隐藏开头标记。

所以 AI 读写文件时，不应该靠猜，而应该明确写：

```python
Path("file.txt").read_text(encoding="utf-8")
```

CSV 如果可能带 BOM，可以用：

```python
open("manifest.csv", "r", encoding="utf-8-sig", newline="")
```

## 5. 为什么不建议一上来就强行改控制台编码

看到乱码时，很多人第一反应是强制设置 UTF-8：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

但在某些 AI 编程工具里，这样反而可能让工具捕获到的输出更乱。

更稳的做法是：

- 文件读写时显式指定编码。
- 命令输出先小范围测试。
- 不为了“看起来像 UTF-8”就盲目改整个控制台。

这也是这个 Skill 的默认规则：先验证，再改变。

## 6. 环境探测脚本看什么

运行：

```powershell
python skills/environment-aware-self-correction/scripts/probe_environment.py --project-root . --pretty
```

你会看到一份 JSON。新手不需要全懂，重点看它回答了这些问题：

- 当前是什么系统。
- Python 是哪个版本、在哪里。
- 默认编码是什么。
- 项目里有没有大量中文路径。
- Git、Docker、Node、GitHub CLI 在不在。
- 当前目录是不是 Git 仓库。
- Docker 服务有没有跑起来。

它不是为了炫技，而是为了让 AI 在动手前少猜。

## 7. 怎么指挥 AI 使用这个 Skill

当你发现 AI 又开始猜环境，可以直接说：

```text
先别继续，使用 environment-aware-self-correction 探测本机环境。
```

当它重复犯错，可以说：

```text
把这次错误写成纠错经验：以后在 PowerShell 里不要用 Bash heredoc。
```

当你不确定为什么命令失败，可以说：

```text
先判断这是 shell 语法问题、编码问题、路径问题，还是服务没有启动。
```

## 8. 给新手的判断顺序

遇到 AI 命令失败，不要急着换一条命令。先按这个顺序看：

1. 是不是 Shell 写法错了。
2. 是不是路径里有中文、空格或特殊符号。
3. 是不是读写文件时编码没写清楚。
4. 是不是服务还没启动或端口不对。
5. 是不是 Git、Docker、Node、Python 这些工具根本没装好。

这个顺序很朴素，但很有用。它能把“玄学报错”变成“逐项排查”。

## 9. 为什么这不会影响正常使用

这个 Skill 把内容分成两层：

- AI 平时执行，只读短规则和必要脚本。
- 人想学习时，再读这份中文说明。

也就是说，它不是让 AI 每次都上一堂长课，而是让 AI 有一张稳定的检查清单；新手需要理解时，再打开讲解版慢慢看。

## 10. 最重要的三句话

1. 不要让 AI 直接猜你的电脑环境。
2. 中文路径和编码问题要显式处理。
3. AI 犯过的错，要让它写成规则，下次先检查。

这就是这个 Skill 的核心价值。

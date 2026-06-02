# 环境感知纠错 Skill

这是一个给 Codex / AI 编程助手使用的技能：**先看清本机环境，再写命令、改文件、启动服务**。

它主要解决一种很常见、也很烦人的问题：AI 写代码时经常把你的电脑环境想当然。比如把 Windows PowerShell 当成 Bash，把中文路径当成普通英文路径，把 UTF-8、GBK、cp936 混着用，结果命令一跑就炸。

这个 Skill 的作用不是让新手背命令，而是让 AI 先做“开工前体检”，少猜、少错、少重复踩坑。

## 适合谁

这个仓库主要面向中文用户，尤其是刚开始用 AI 编程的人。

你不需要先学会 Shell、编码、Git 或 Docker。你只要知道一件事：

> AI 不是直接住在你的电脑里，它也要先搞清楚你的电脑是什么环境。

## 一句话理解

可以把这个 Skill 理解成 AI 的“开工前检查清单”：

1. 先确认当前是什么系统和命令行。
2. 再选择正确命令写法。
3. 先小范围验证一下。
4. 再真正改代码、跑脚本或启动服务。
5. 如果犯错，把经验记下来，下次别再犯。

## 只想用，怎么做

在项目根目录执行：

```powershell
python skills/environment-aware-self-correction/scripts/probe_environment.py --project-root . --pretty
```

如果你正在和 AI 编程助手协作，可以直接对它说：

```text
先使用 environment-aware-self-correction 检查本机环境，再继续执行。
```

如果它又在 PowerShell、中文路径、UTF-8/GBK、Docker 服务、GitHub 发布这些地方翻车，可以说：

```text
把这次错误写成纠错经验：以后先判断 shell、编码、路径和服务状态，不要直接猜。
```

## 它能避免哪些坑

- AI 在 PowerShell 里写 Bash 命令，例如 `python - <<'PY'`。
- 中文文件名、中文目录被命令误拆、误匹配或显示乱码。
- UTF-8、GBK、cp936 编码混用导致 CSV、JSON、Markdown 读写异常。
- 服务还没启动完成，AI 就误判为“接口坏了”。
- Docker、Git、GitHub CLI 是否存在没有先检查。
- 用户已经纠正过的问题，下一次 AI 又原样犯。

## 为什么不把说明全塞进 SKILL.md

因为 `SKILL.md` 是 AI 真正执行技能时会读取的文件。它应该短、准、可执行。

如果把大量新手解释全部写进去，AI 每次工作都会读一堆“教材内容”，上下文会变重，执行反而可能变慢、变钝。

所以这里采用分层设计：

- `SKILL.md`：给 AI 执行用，保持短规则。
- `README.md`：给人快速入门，适合 GitHub 首页。
- `references/beginner-guide-zh.md`：给中文新手慢慢看，解释“为什么会错”。
- `references/windows-powershell-encoding.md`：给需要深挖 Windows、PowerShell、中文编码问题时再读。
- `scripts/probe_environment.py`：真正做环境探测的脚本。

这样既不影响 AI 使用，又能让刚入门的人看懂、搞懂。

## 给新手的三个关键词

**Shell**：你输入命令的地方。PowerShell、cmd、Bash 语法不一样。

**路径**：文件在哪里。中文路径、空格、特殊符号都要认真处理。

**编码**：文字怎么保存和读取。中文乱码大多和编码有关。

只要 AI 在动手前先检查这三个东西，很多低级但折磨人的错误就能少很多。

## 仓库地址

https://github.com/iasgu/environment-aware-self-correction

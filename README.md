# 环境感知纠错 Skill

这是一套给 Codex / AI 编程助手用的“先看环境，再动手”的技能。

它解决一个很常见的问题：AI 写代码时，经常会把本机环境想当然，比如把 Windows PowerShell 当成 Bash，把中文路径当成普通英文路径，把 UTF-8 和 GBK 混着用，结果命令一跑就炸。这个 Skill 的作用，就是让 AI 在容易出错前先检查本机环境，并把踩过的坑记成规则。

## 适合谁

这份仓库主要面向中文用户，尤其是刚开始用 AI 编程的人。你不需要先懂 Shell、编码、Git 或 Docker，只要知道一件事：

> AI 不是万能的，它也需要先搞清楚你的电脑是什么环境。

## 它能帮你避免什么

- AI 在 PowerShell 里写 Bash 命令。
- 中文文件名、中文目录被命令搞坏。
- UTF-8、GBK、cp936 编码互相打架。
- Python 读 CSV 时表头多出奇怪字符。
- 本地服务还没启动完，AI 就误判“服务失败”。
- 用户已经纠正过的问题，下一次 AI 又犯。

## 一句话理解

可以把它理解成 AI 的“开工前检查清单”：

1. 先确认电脑环境。
2. 再选择正确命令。
3. 小范围验证一下。
4. 真正开始改代码或运行脚本。
5. 如果犯错，把经验记下来，下次别再犯。

## 文件怎么读

- `SKILL.md`：给 AI 看的核心规则。越短越好，不建议初学者从这里开始读。
- `README.md`：你现在看到的文件，给人看的入门说明。
- `references/beginner-guide-zh.md`：更详细的新手解释，讲清楚为什么会出错、怎么判断。
- `references/windows-powershell-encoding.md`：Windows、PowerShell、中文编码专项说明。
- `scripts/probe_environment.py`：环境探测脚本，会输出当前机器的 Python、Git、Docker、路径和编码情况。

## 怎么运行环境探测

在项目根目录执行：

```powershell
python skills/environment-aware-self-correction/scripts/probe_environment.py --project-root . --pretty
```

你会看到一份 JSON。初学者不用全部看懂，重点看这些字段：

- `platform`：你是什么系统。
- `python`：Python 在哪里、默认编码是什么。
- `project.non_ascii_paths.count`：项目里有多少中文路径或非英文路径。
- `tools`：有没有 Git、Docker、Node、GitHub CLI。
- `git.ok`：当前目录是不是 Git 仓库。
- `docker.ok`：Docker 是否可用。

## 给新手的使用建议

如果你发现 AI 连续犯同一种错，可以直接对它说：

```text
先用 environment-aware-self-correction 检查环境，再继续。
```

或者：

```text
你刚才又在 PowerShell / 中文路径 / UTF-8 上犯错了，把这个纠错经验写进规则里。
```

这会提醒 AI 先停下来，不要继续猜。

## 为什么不把所有说明都写进 SKILL.md

因为 `SKILL.md` 是 AI 每次触发技能时真正会读的文件。如果写得太长，AI 会被大量入门解释占用上下文，反而影响执行效率。

所以这里采用分层设计：

- AI 执行时读短规则。
- 人学习时读中文说明。
- 需要深入时再读 reference 文件。

这样既不影响使用，也更容易看懂。

## 仓库地址

https://github.com/iasgu/environment-aware-self-correction

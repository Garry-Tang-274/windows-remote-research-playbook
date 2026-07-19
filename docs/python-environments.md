# Python 环境排障
# Python Environment Troubleshooting

## 先确认解释器
## Confirm the Interpreter First

同一台 Windows 电脑可能同时存在 Microsoft Store Python、官网 Python、Conda、虚拟环境和编辑器内解释器。

The same Windows computer may contain Microsoft Store Python, python.org Python, Conda, virtual environments, and editor-selected interpreters at the same time.

运行以下命令记录实际路径和版本。

Run the following commands to record the actual path and version.

```powershell
where.exe python
where.exe py
py -0p
python --version
python -c "import sys; print(sys.executable)"
```

安装成功不等于当前终端正在使用正确解释器。

A successful installation does not mean the current terminal is using the intended interpreter.

## 虚拟环境
## Virtual Environments

每个科研项目建议使用独立环境，并在 README 中记录创建、激活和安装命令。

Each research project should use an isolated environment, with creation, activation, and installation commands recorded in the README.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

若 PowerShell 阻止激活脚本，先了解执行策略并只对当前用户做最小必要修改；不要在不了解风险时全局关闭策略。

If PowerShell blocks the activation script, understand execution policies and make only the minimum required change for the current user; do not disable policy globally without understanding the risk.

## 包安装位置
## Package Installation Location

使用 `python -m pip` 比直接使用 `pip` 更容易确保包安装到当前解释器。

Using `python -m pip` makes it easier to ensure that packages are installed into the current interpreter than invoking `pip` directly.

```powershell
python -m pip --version
python -m pip show package_name
```

出现 `ModuleNotFoundError` 时，同时检查运行脚本的解释器和安装包的解释器，而不是反复重装。

When `ModuleNotFoundError` occurs, inspect both the interpreter running the script and the interpreter receiving the package instead of repeatedly reinstalling.

## 远程环境
## Remote Environments

编辑器连接服务器后，终端和 Python 扩展应选择服务器上的解释器，而不是本地 Windows 路径。

After an editor connects to a server, the terminal and Python extension should select an interpreter on the server rather than a local Windows path.

记录 `hostname`、`pwd`、`which python` 和 `python -c "import sys; print(sys.executable)"` 可以快速确认当前执行位置。

Recording `hostname`, `pwd`, `which python`, and `python -c "import sys; print(sys.executable)"` quickly confirms where execution is occurring.

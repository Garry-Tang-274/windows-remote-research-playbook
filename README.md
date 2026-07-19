# Windows 远程科研开发排障手册
# Windows Remote Research Development Playbook

这是一个面向使用 Windows 连接 Linux 科研服务器的学生与初学者的实用手册，覆盖 SSH、校园 VPN、编辑器远程连接、Python 环境和信息脱敏。

This is a practical playbook for students and beginners who use Windows to connect to Linux research servers, covering SSH, campus VPNs, remote editor connections, Python environments, and information redaction.

手册强调先建立可重复的诊断顺序，再更改配置；每一步都说明目的、命令、预期结果和失败后的下一步。

The playbook emphasizes establishing a repeatable diagnostic order before changing configuration; each step explains its purpose, command, expected result, and next action after failure.

## 使用边界
## Scope and Boundaries

本文档不提供绕过学校安全策略、管理员限制或访问控制的方法。所有操作都应在你有权使用的账号、网络和服务器上进行。

These documents do not provide methods to bypass school security policies, administrator restrictions, or access controls. All operations should be performed only on accounts, networks, and servers you are authorized to use.

在公开 Issue 或截图前，必须隐藏服务器地址、用户名、邮箱、目录、令牌、Cookie、VPN 域名和研究数据文件名。

Before posting an issue or screenshot publicly, redact server addresses, usernames, email addresses, directories, tokens, cookies, VPN domains, and research-data filenames.

## 推荐排障顺序
## Recommended Troubleshooting Order

第一步确认本机网络和目标端口是否可达；第二步在 PowerShell 中直接运行 SSH；第三步才检查 VS Code、Zed 或其他编辑器；最后处理 Python 环境和项目依赖。

First confirm local network and target-port reachability; second run SSH directly in PowerShell; third inspect VS Code, Zed, or another editor; finally address Python environments and project dependencies.

不要同时更换 VPN、SSH 配置、编辑器扩展和 Python 环境，否则即使问题消失也无法判断根因。

Do not change the VPN, SSH configuration, editor extension, and Python environment simultaneously, because even if the problem disappears, the root cause will remain unknown.

## 快速诊断
## Quick Diagnosis

在 PowerShell 中运行以下脚本，其中参数应替换为你自己的授权目标。

Run the following script in PowerShell, replacing the parameters with your own authorized target.

```powershell
.\scripts\check_ssh_connection.ps1 -HostName example.edu -Port 22
```

收集可公开分享的本机环境摘要时运行以下命令。脚本默认不会导出密码、令牌或 SSH 私钥。

Run the following command to collect a local environment summary that can be shared publicly. By default, the script does not export passwords, tokens, or SSH private keys.

```powershell
.\scripts\collect_environment_info.ps1
```

检查 Python 解释器、虚拟环境和包管理器时运行以下命令。

Run the following command to inspect Python interpreters, virtual environments, and package managers.

```powershell
.\scripts\check_python_environment.ps1
```

## 文档导航
## Documentation Map

- `docs/ssh-diagnosis.md`：从网络到认证的 SSH 排查顺序。
- `docs/ssh-diagnosis.md`: SSH troubleshooting from network reachability to authentication.
- `docs/vpn-routing.md`：规则模式、全局模式、DNS 和路由冲突。
- `docs/vpn-routing.md`: Rule mode, global mode, DNS, and routing conflicts.
- `docs/python-environments.md`：解释器、虚拟环境、路径与依赖问题。
- `docs/python-environments.md`: Interpreters, virtual environments, paths, and dependency issues.
- `docs/vscode-remote.md`：VS Code Remote SSH 的分层排查。
- `docs/vscode-remote.md`: Layered troubleshooting for VS Code Remote SSH.
- `docs/zed-remote.md`：Zed 远程连接与终端差异。
- `docs/zed-remote.md`: Zed remote connections and terminal differences.
- `docs/security-redaction.md`：日志与截图脱敏清单。
- `docs/security-redaction.md`: Redaction checklist for logs and screenshots.

## 贡献原则
## Contribution Principles

新增命令必须说明适用系统、是否修改状态、是否需要管理员权限，以及如何撤销。

Every new command must state the applicable system, whether it modifies state, whether administrator privileges are required, and how to undo it.

所有文档保持严格段落对应的中英双语；命令本身只写一次，但其用途和结果必须双语解释。

All documents must maintain strictly paragraph-corresponding Chinese and English; commands appear only once, but their purpose and results must be explained bilingually.

## 许可
## License

本手册与脚本采用 MIT 许可证。执行命令前应理解其作用，并对自己的系统和数据负责。

This playbook and its scripts are licensed under the MIT License. Understand each command before running it and remain responsible for your own system and data.

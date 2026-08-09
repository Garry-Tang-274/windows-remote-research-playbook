# Windows 远程科研开发排障手册
# Windows Remote Research Development Playbook

![Status](https://img.shields.io/badge/status-maintained-2f81f7)
![Scope](https://img.shields.io/badge/scope-research%20engineering-8957e5)
![Language](https://img.shields.io/badge/docs-bilingual-d8aa56)
![License](https://img.shields.io/badge/license-MIT-3fb950)

这是一本面向学生和初学者的远程科研开发手册，覆盖 Windows 到 Linux 服务器的连接、校园 VPN、FlClash / TUN / 系统代理、远程编辑器、Python 环境、GitHub 发布、信息脱敏，以及独立的 Android 网络排障附录。

This is a remote research-development playbook for students and beginners, covering Windows-to-Linux server access, campus VPNs, FlClash / TUN / system-proxy troubleshooting, remote editors, Python environments, GitHub publishing, information redaction, and a separate Android networking appendix.

> **核心方法：** 先定位故障层级，再一次只改变一个变量；记录修改前现象、唯一改动、预期结果和实际结果。
>
> **Core method:** Identify the failing layer first, then change one variable at a time; record the initial symptom, the single change, the expected result, and the observed result.

[SSH 排障](docs/ssh-diagnosis.md) · [Windows FlClash / TUN](docs/windows-flclash-routing.md) · [VPN 路由](docs/vpn-routing.md) · [Python 环境](docs/python-environments.md) · [GitHub 发布](docs/github-repository-publishing.md) · [安全脱敏](docs/security-redaction.md) · [个人主页](https://garry-tang-274.github.io)

[SSH diagnosis](docs/ssh-diagnosis.md) · [Windows FlClash / TUN](docs/windows-flclash-routing.md) · [VPN routing](docs/vpn-routing.md) · [Python environments](docs/python-environments.md) · [GitHub publishing](docs/github-repository-publishing.md) · [Security redaction](docs/security-redaction.md) · [Portfolio](https://garry-tang-274.github.io)

## 推荐排障顺序
## Recommended Troubleshooting Order

远程服务器问题应先确认本机网络和目标端口是否可达；第二步在 PowerShell 中直接运行 SSH；第三步检查 VS Code、Zed 或其他编辑器；最后处理 Python 环境和项目依赖。

For remote-server problems, first confirm local network and target-port reachability; second run SSH directly in PowerShell; third inspect VS Code, Zed, or another editor; finally address Python environments and project dependencies.

Windows 代理问题优先回到“规则模式 + 系统代理开 + TUN 关”的诊断基线，再分别测试国内网站、GitHub / ChatGPT、桌面应用和 SSH。不要用网页是否正常来推断桌面应用或 SSH 一定走同一条路径。

For Windows proxy problems, first return to the diagnostic baseline of rule mode with the system proxy enabled and TUN disabled, then test domestic websites, GitHub / ChatGPT, desktop applications, and SSH separately. Do not infer that desktop applications or SSH use the same path merely because the web works.

GitHub 发布问题应先确认操作环境与权限，再区分少量文件写入、Git Tree 批量提交和本机 Git 推送；完成后重新读取关键文件，并检查临时恢复内容是否已经清理。

For GitHub publishing problems, first confirm the operating environment and permission scope, then distinguish small-file writes, Git Tree batch commits, and local Git pushes; afterward, reread key files and verify that temporary restoration content has been removed.

Android 代理问题应依次确认 VPN 会话、分应用路由、规则模式、节点、DNS 与后台存活，不要同时修改所有层级。

For Android proxy problems, verify the VPN session, per-app routing, rule mode, node, DNS, and background survival in sequence; do not change all layers simultaneously.

## 快速诊断
## Quick Diagnosis

检查目标端口与 SSH 连接：

Check target-port reachability and SSH connectivity:

```powershell
.\scripts\check_ssh_connection.ps1 -HostName example.edu -Port 22
```

Windows 上遇到“国内正常、GitHub / GPT 很慢”或“开 TUN 后全网更差”时，直接进入 FlClash / TUN 专项文档，并按 A/B/C 三组状态做对照。

On Windows, when domestic sites work but GitHub / GPT is very slow, or enabling TUN makes the whole network worse, go directly to the FlClash / TUN guide and compare the A/B/C states.

[`docs/windows-flclash-routing.md`](docs/windows-flclash-routing.md)

收集可公开分享的本机环境摘要。脚本默认不会导出密码、令牌或 SSH 私钥：

Collect a local environment summary suitable for public sharing. By default, the script does not export passwords, tokens, or SSH private keys:

```powershell
.\scripts\collect_environment_info.ps1
```

检查 Python 解释器、虚拟环境和包管理器：

Inspect Python interpreters, virtual environments, and package managers:

```powershell
.\scripts\check_python_environment.ps1
```

检查 GitHub CLI 登录状态与仓库访问权限：

Check GitHub CLI authentication and repository access:

```powershell
gh auth status
gh repo view OWNER/REPOSITORY
```

## 最近补充的实战内容
## Recent Practical Additions

### Windows FlClash、TUN 与系统代理
### Windows FlClash, TUN, and System Proxy

[`docs/windows-flclash-routing.md`](docs/windows-flclash-routing.md) 新增了最近实际遇到的两类故障模式：系统代理开启、TUN 关闭时国内网站正常但 GitHub / ChatGPT 很慢；以及开启 TUN 后整个网络进一步变慢或不稳定。文档还覆盖网页正常但桌面应用 / Remote 异常、TUN 前后路由与 DNS 对照、DNS 缓存恢复和 SSH 独立测试。

[`docs/windows-flclash-routing.md`](docs/windows-flclash-routing.md) adds two recently observed failure patterns: domestic sites work with the system proxy enabled and TUN disabled while GitHub / ChatGPT is very slow, and enabling TUN makes the overall network even slower or unstable. It also covers web-versus-desktop / Remote differences, route and DNS comparisons before and after TUN, DNS-cache recovery, and separate SSH testing.

### GitHub 仓库发布与完整性验证
### GitHub Repository Publishing and Integrity Verification

[`docs/github-repository-publishing.md`](docs/github-repository-publishing.md) 说明网页端、连接器、本机 Git 与 GitHub CLI 的职责边界，并覆盖仓库创建权限、批量提交、Actions 未触发、完整性验证和临时文件清理。

[`docs/github-repository-publishing.md`](docs/github-repository-publishing.md) explains the boundaries between the website, connectors, local Git, and GitHub CLI, covering repository-creation permissions, batch commits, Actions not triggering, integrity verification, and temporary-file cleanup.

### Android Clash 分流与后台存活
### Android Clash Split Tunneling and Background Survival

[`docs/android-clash-split-tunneling.md`](docs/android-clash-split-tunneling.md) 区分分应用路由与规则模式，解释允许列表、拒绝列表、系统组件、VPN 会话重启和后台限制。

[`docs/android-clash-split-tunneling.md`](docs/android-clash-split-tunneling.md) separates per-app routing from rule mode and explains allowlists, denylists, system components, VPN-session restarts, and background restrictions.

## 文档导航
## Documentation Map

- [`docs/ssh-diagnosis.md`](docs/ssh-diagnosis.md)：从网络到认证的 SSH 排查顺序，并区分浏览器、系统代理、TUN 与 SSH 的网络路径。
- [`docs/ssh-diagnosis.md`](docs/ssh-diagnosis.md): SSH troubleshooting from network reachability to authentication, including browser, system-proxy, TUN, and SSH path differences.
- [`docs/windows-flclash-routing.md`](docs/windows-flclash-routing.md)：Windows FlClash、系统代理、TUN、桌面应用与 SSH 的专项排障。
- [`docs/windows-flclash-routing.md`](docs/windows-flclash-routing.md): Focused troubleshooting for Windows FlClash, the system proxy, TUN, desktop applications, and SSH.
- [`docs/vpn-routing.md`](docs/vpn-routing.md)：规则模式、全局模式、DNS、系统代理和路由冲突。
- [`docs/vpn-routing.md`](docs/vpn-routing.md): Rule mode, global mode, DNS, system-proxy, and routing conflicts.
- [`docs/python-environments.md`](docs/python-environments.md)：解释器、虚拟环境、路径与依赖问题。
- [`docs/python-environments.md`](docs/python-environments.md): Interpreters, virtual environments, paths, and dependency problems.
- [`docs/vscode-remote.md`](docs/vscode-remote.md)：VS Code Remote SSH 的分层排查。
- [`docs/vscode-remote.md`](docs/vscode-remote.md): Layered troubleshooting for VS Code Remote SSH.
- [`docs/zed-remote.md`](docs/zed-remote.md)：Zed 远程连接与终端差异。
- [`docs/zed-remote.md`](docs/zed-remote.md): Zed remote connections and terminal differences.
- [`docs/github-repository-publishing.md`](docs/github-repository-publishing.md)：GitHub 发布、批量提交与完整性验证。
- [`docs/github-repository-publishing.md`](docs/github-repository-publishing.md): GitHub publishing, batch commits, and integrity verification.
- [`docs/android-clash-split-tunneling.md`](docs/android-clash-split-tunneling.md)：Android 分应用路由、规则模式和后台存活。
- [`docs/android-clash-split-tunneling.md`](docs/android-clash-split-tunneling.md): Android per-app routing, rule mode, and background survival.
- [`docs/security-redaction.md`](docs/security-redaction.md)：日志与截图脱敏清单。
- [`docs/security-redaction.md`](docs/security-redaction.md): Redaction checklist for logs and screenshots.

## 使用边界
## Scope and Boundaries

本文档不提供绕过学校安全策略、管理员限制、仓库保护规则、地区限制或访问控制的方法。所有操作都应仅用于你有权使用的账号、网络、服务器和仓库。

These documents do not provide methods to bypass school security policies, administrator restrictions, repository protection rules, regional restrictions, or access controls. All operations should be performed only on accounts, networks, servers, and repositories you are authorized to use.

公开 Issue、日志或截图前，必须隐藏服务器地址、用户名、邮箱、目录、令牌、Cookie、VPN 域名、节点订阅、研究数据文件名和私有仓库信息。

Before posting an issue, log, or screenshot publicly, redact server addresses, usernames, email addresses, directories, tokens, cookies, VPN domains, proxy subscriptions, research-data filenames, and private-repository information.

## 贡献原则
## Contribution Principles

新增命令必须说明适用系统、是否修改状态、是否需要管理员权限，以及如何撤销。

Every new command must state the applicable system, whether it modifies state, whether administrator privileges are required, and how to undo it.

所有文档保持严格段落对应的中英双语；真实排障经验必须区分已确认根因、合理推测和仍未确定的现象。

All documents maintain strictly corresponding Chinese and English paragraphs; real troubleshooting experience must distinguish confirmed root causes, reasonable hypotheses, and unresolved observations.

## 许可
## License

本手册与脚本采用 MIT 许可证。执行命令前应理解其作用，并对自己的系统、仓库和数据负责。

This playbook and its scripts are licensed under the MIT License. Understand each command before running it and remain responsible for your own system, repositories, and data.

# SSH 分层排障
# Layered SSH Troubleshooting

## 第 1 层：确认目标与网络
## Layer 1: Confirm the Target and Network

先确认服务器主机名、端口、用户名和是否必须连接校园网或 VPN。不要从旧截图猜测这些信息。

First confirm the server hostname, port, username, and whether campus networking or a VPN is required. Do not guess these values from an old screenshot.

运行端口测试可以区分“服务器不可达”和“SSH 认证失败”。

A port test distinguishes “server unreachable” from “SSH authentication failed.”

```powershell
Test-NetConnection example.edu -Port 22
```

若 `TcpTestSucceeded` 为 `False`，优先检查 VPN、路由、防火墙、服务器维护和端口，而不是修改密码或密钥。

If `TcpTestSucceeded` is `False`, inspect VPN, routing, firewalls, server maintenance, and the port before changing passwords or keys.

## 第 2 层：直接运行 SSH
## Layer 2: Run SSH Directly

编辑器远程连接建立在 SSH 之上，因此应先在 PowerShell 中验证基础命令。

Editor remote connections are built on SSH, so validate the basic command in PowerShell first.

```powershell
ssh -vvv username@example.edu
```

`-vvv` 会输出详细阶段。公开日志前删除主机名、用户名、IP、密钥路径和任何令牌。

`-vvv` prints detailed stages. Before sharing logs publicly, remove hostnames, usernames, IP addresses, key paths, and any tokens.

若停在连接阶段，问题通常位于网络；若出现 `Permission denied`，问题通常位于账号、密码、密钥或服务器认证策略。

If the command stalls during connection, the problem is usually network-related; if it shows `Permission denied`, the problem is usually the account, password, key, or server authentication policy.

## 第 3 层：检查 SSH 配置
## Layer 3: Inspect SSH Configuration

Windows OpenSSH 通常读取 `%USERPROFILE%\.ssh\config`。配置别名可以减少编辑器与终端之间的差异。

Windows OpenSSH usually reads `%USERPROFILE%\.ssh\config`. A host alias can reduce differences between editors and terminals.

```sshconfig
Host research-server
    HostName example.edu
    User username
    Port 22
```

先使用 `ssh research-server` 验证配置，再让编辑器选择同一个别名。

Validate the configuration with `ssh research-server` before selecting the same alias in the editor.

## 第 4 层：认证与权限
## Layer 4: Authentication and Permissions

密码能在终端使用但编辑器失败时，应检查编辑器是否调用了不同的 SSH 程序、配置文件或密钥代理。

If the password works in a terminal but the editor fails, check whether the editor uses a different SSH executable, configuration file, or key agent.

密钥认证失败时，检查私钥路径、公钥是否安装到正确账号、服务器文件权限和密钥算法是否被允许。

When key authentication fails, inspect the private-key path, whether the public key is installed for the correct account, server file permissions, and whether the key algorithm is allowed.

不要把私钥内容、恢复码或一次性验证码发到 Issue、聊天或截图中。

Never post private-key contents, recovery codes, or one-time passwords in issues, chats, or screenshots.

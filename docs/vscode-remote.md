# VS Code Remote SSH 排障
# VS Code Remote SSH Troubleshooting

## 前置条件
## Prerequisites

在打开 VS Code 前，先确保 PowerShell 中的 `ssh host-alias` 可以稳定登录。

Before opening VS Code, ensure that `ssh host-alias` logs in reliably from PowerShell.

若基础 SSH 不通，反复重装 Remote SSH 扩展通常不会解决问题。

If basic SSH does not work, repeatedly reinstalling the Remote SSH extension usually will not solve the problem.

## 分层检查
## Layered Checks

确认 VS Code 使用的 SSH 配置文件与 PowerShell 相同，并检查 Remote SSH 输出面板中的实际命令。

Confirm that VS Code uses the same SSH configuration file as PowerShell and inspect the actual command in the Remote SSH output panel.

连接成功但目录打不开时，检查远程路径权限、磁盘空间、Shell 启动脚本和服务器端 VS Code 组件。

If connection succeeds but a directory cannot open, inspect remote-path permissions, disk space, shell startup scripts, and the server-side VS Code component.

终端可用但 Python 运行错误时，重新选择远程解释器，并确认窗口左下角显示远程主机。

If the terminal works but Python execution fails, select the remote interpreter again and confirm that the lower-left corner shows the remote host.

## 日志共享
## Sharing Logs

共享 Remote SSH 日志前删除主机名、用户名、IP、目录、密钥路径和环境变量值。

Before sharing Remote SSH logs, remove hostnames, usernames, IP addresses, directories, key paths, and environment-variable values.

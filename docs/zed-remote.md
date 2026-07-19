# Zed 远程连接排障
# Zed Remote Connection Troubleshooting

## 与终端结果对齐
## Align with Terminal Results

Zed 远程连接也依赖底层 SSH。PowerShell 秒连而 Zed 长时间转圈时，重点比较二者使用的主机别名、SSH 程序、认证方法和配置文件。

Zed remote connections also depend on underlying SSH. If PowerShell connects immediately while Zed spins for a long time, compare the host alias, SSH executable, authentication method, and configuration file used by each.

不要因为编辑器卡住就立刻判断服务器宕机；先重复端口测试和命令行 SSH。

Do not immediately assume the server is down because the editor stalls; repeat the port test and command-line SSH first.

## 项目与终端
## Project and Terminal

确认打开的是远程目录而不是本地同名目录，并在集成终端运行 `hostname` 与 `pwd`。

Confirm that the opened directory is remote rather than a local directory with the same name, and run `hostname` and `pwd` in the integrated terminal.

快捷键没有反应时，应先查看当前键位配置和命令面板，而不是把运行失败归因于 Python。

If a shortcut does nothing, inspect the active keymap and command palette before attributing the failure to Python.

## 失败记录
## Failure Record

记录发生时间、网络状态、命令行 SSH 结果、Zed 版本和最后可见日志，可以帮助区分偶发网络问题与稳定配置问题。

Record the time, network state, command-line SSH result, Zed version, and last visible log to distinguish intermittent network problems from persistent configuration problems.

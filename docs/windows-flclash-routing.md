# Windows FlClash、TUN 与系统代理排障
# Windows FlClash, TUN, and System Proxy Troubleshooting

这篇文档整理 Windows 上 FlClash、系统代理、TUN、浏览器、桌面应用与 SSH 同时存在时的排障方法。重点不是“哪个开关永远正确”，而是先确认每类流量实际走哪条网络路径。

This guide covers troubleshooting when FlClash, the Windows system proxy, TUN mode, browsers, desktop applications, and SSH coexist. The goal is not to find one permanently correct switch combination, but to identify the actual network path used by each type of traffic.

FlClash 是基于 ClashMeta 的多平台客户端；Windows 版本支持系统代理与 TUN。具体界面和行为可能随版本变化，因此本文只依赖这些稳定概念，不依赖某一个版本的按钮位置。

FlClash is a multi-platform client based on ClashMeta; its Windows version supports both a system proxy and TUN. UI placement and details may change between versions, so this guide relies on stable concepts rather than one specific layout.

## 先区分四条网络路径
## First Separate Four Network Paths

浏览器通常可以使用 Windows 系统代理；某些桌面应用可能完全使用系统代理、部分使用系统代理，或直接建立连接；TUN 会在更底层接管更多流量；SSH 通常不会因为打开 HTTP 系统代理就自动走代理。

Browsers can usually use the Windows system proxy; some desktop applications may fully use it, partially use it, or connect directly; TUN captures traffic at a lower layer; SSH normally does not start using an HTTP system proxy merely because that proxy is enabled.

因此，“网页能打开”不能证明桌面应用也走通了，“ChatGPT 网页正常”也不能证明桌面端 Remote 路径正常，“GitHub 网页正常”更不能证明 SSH 到科研服务器正常。

Therefore, “the website opens” does not prove that the desktop application has a working path; a working ChatGPT web session does not prove that a desktop Remote path works; and a working GitHub website does not prove SSH reachability to a research server.

## 推荐基线：规则模式 + 系统代理开 + TUN 关
## Recommended Baseline: Rule Mode + System Proxy On + TUN Off

在 Windows 桌面端遇到网络异常时，建议先回到一个最容易解释的基线：FlClash 使用规则模式，系统代理开启，TUN 关闭。此时先只验证浏览器和普通 HTTPS 流量。

When Windows desktop networking becomes unstable, first return to a baseline that is easy to reason about: use rule mode in FlClash, enable the system proxy, and disable TUN. At this stage, validate only browser and ordinary HTTPS traffic.

这个基线不是永久推荐配置，而是诊断起点。若此时国内网站正常，而 GitHub、ChatGPT 等外部站点明显变慢或无法访问，至少说明本机基础网络仍然可用，下一步应优先检查节点、规则命中、DNS 和代理链路，而不是立刻重置 Windows 网络。

This baseline is a diagnostic starting point, not a permanent recommendation. If domestic websites work normally while external sites such as GitHub or ChatGPT become very slow or unreachable, the underlying local network is at least still usable; inspect the node, rule matching, DNS, and proxy path before resetting Windows networking.

## 建立三组对照
## Build Three Controlled States

每次只测试一个状态，并记录结果。不要同时换节点、开 TUN、改 DNS 和切全局模式。

Test one state at a time and record the result. Do not change the node, enable TUN, modify DNS, and switch to global mode at the same time.

### A：代理与 TUN 都关闭
### A: Proxy and TUN Both Off

用于确认本机 Wi-Fi、有线网络和国内网络是否本身正常。此状态不用于判断需要代理才能访问的站点是否“应该能打开”。

Use this state to confirm that the local Wi-Fi or Ethernet connection and ordinary domestic connectivity are healthy. Do not use it to decide whether sites that require a proxy path “should work.”

### B：规则模式，系统代理开启，TUN 关闭
### B: Rule Mode, System Proxy On, TUN Off

这是 Windows 上最适合作为第一基线的状态。若浏览器正常而某个桌面应用失败，说明应用与浏览器可能没有使用同一条网络路径。

This is the best first baseline on Windows. If the browser works but a desktop application fails, the application and browser may not be using the same network path.

### C：在 B 的基础上临时开启 TUN
### C: Temporarily Enable TUN on Top of B

只在需要判断“该应用是否绕过系统代理”时短暂测试。若开启 TUN 后目标应用恢复，但国内网站、GitHub 或其他程序整体变慢、超时或不稳定，不应把 TUN 当作永久修复；应继续排查 TUN 路由、DNS、虚拟网卡或客户端状态。

Use this only as a temporary test when you need to determine whether an application bypasses the system proxy. If the target application starts working after TUN is enabled but domestic websites, GitHub, or other programs become slow, time out, or unstable, do not treat TUN as a permanent fix; continue investigating TUN routing, DNS, the virtual adapter, or client state.

## 最近遇到的典型现象
## Recent Representative Symptoms

### 国内网站正常，但 GitHub / ChatGPT 很慢
### Domestic Sites Work, but GitHub / ChatGPT Are Very Slow

若系统代理已经开启、TUN 关闭，并且国内网站流畅，而 GitHub 或 ChatGPT 很慢或完全打不开，优先把问题缩小到代理侧。先看 FlClash 的连接、请求或日志页面是否出现这些域名，再只更换一个节点测试，不要同时调整 DNS 和规则。

If the system proxy is enabled, TUN is disabled, and domestic websites are fast while GitHub or ChatGPT is very slow or unreachable, narrow the problem to the proxy side first. Check whether the relevant domains appear in FlClash connections, requests, or logs, then test one different node without changing DNS and rules at the same time.

可以用以下只读测试区分 DNS、TCP 和 HTTP 层。`curl.exe` 收到任何明确的 HTTP 响应都说明 TLS/HTTP 路径已经建立，不要求必须返回 `200`。

The following read-only tests help separate DNS, TCP, and HTTP layers. Any explicit HTTP response from `curl.exe` means the TLS/HTTP path was established; a `200` response is not required.

```powershell
Resolve-DnsName github.com
Test-NetConnection github.com -Port 443
curl.exe -I https://github.com
```

### 开启 TUN 后所有网站都变慢或不稳定
### Enabling TUN Makes the Whole Network Slow or Unstable

这类现象更像 TUN 引入了新的路由、DNS 或虚拟网卡路径，而不是“外网节点单纯太慢”。第一步应关闭 TUN 回到基线 B，确认问题是否立即消失。

This pattern is more consistent with TUN introducing a new routing, DNS, or virtual-adapter path than with a merely slow external node. First disable TUN and return to baseline B to see whether the problem disappears immediately.

以下命令均为只读，可在 TUN 开启前后各运行一次并比较输出。公开日志前必须隐藏接口名称、内部网段和任何可识别的网络信息。

The following commands are read-only. Run them once before enabling TUN and once after enabling it, then compare the output. Redact interface names, internal subnets, and identifying network information before sharing logs publicly.

```powershell
Get-NetAdapter | Sort-Object Status, Name
Get-NetIPConfiguration
Get-DnsClientServerAddress -AddressFamily IPv4
Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric, InterfaceMetric
route print
```

如果关闭 TUN 后仍然表现异常，先完全退出 FlClash 再重新打开；仍有 DNS 异常时，可以执行 `ipconfig /flushdns` 清空本机 DNS 缓存。这个命令会修改缓存状态，但不会修改长期网络配置。

If networking remains abnormal after TUN is disabled, fully exit FlClash and start it again. If DNS behavior is still abnormal, `ipconfig /flushdns` can clear the local DNS cache. This changes cache state but does not modify persistent network configuration.

```powershell
ipconfig /flushdns
```

`netsh winsock reset` 会修改系统网络状态并通常需要管理员权限和重启，不应作为第一步。只有在已经确认关闭客户端、关闭 TUN、重启应用和清理 DNS 都无效时才考虑使用，并在执行前记录当前配置。

`netsh winsock reset` changes system networking state and normally requires administrator privileges and a reboot, so it should not be the first step. Consider it only after closing the client, disabling TUN, restarting the application, and clearing DNS have all failed, and record the current configuration before running it.

## 网页正常，但 ChatGPT 桌面端或 Remote 不正常
## Web Works, but ChatGPT Desktop or Remote Does Not

这种现象不能直接归因于账号或服务器。先把它视为“不同进程可能走不同网络路径”。保持规则模式与系统代理不变，只临时切换 TUN，观察桌面应用是否变化，同时查看 FlClash 的连接、请求或日志中是否出现该应用的目标连接。

Do not attribute this pattern directly to the account or server. Treat it first as “different processes may use different network paths.” Keep rule mode and the system proxy unchanged, toggle only TUN temporarily, observe whether the desktop application changes, and inspect FlClash connections, requests, or logs for the application's target connections.

若只有开启 TUN 时桌面端或 Remote 才能连接，但开启 TUN 又导致全网不稳定，这只能说明 TUN 改变了该应用的路径，不足以证明“必须永久开启 TUN”。应回到基线后继续定位应用代理兼容性和 TUN 路由问题。

If the desktop application or Remote works only when TUN is enabled, but TUN also destabilizes the rest of the network, that shows only that TUN changed the application's path; it does not prove that TUN must remain permanently enabled. Return to the baseline and continue isolating application proxy compatibility and TUN routing.

## SSH 要单独测试
## Test SSH Separately

系统代理主要影响支持该代理设置的 HTTP/HTTPS 应用，不能用浏览器访问结果代替 SSH 测试。科研服务器若要求校园 VPN，应先满足服务器自己的网络条件，再运行端口测试和 `ssh -vvv`。

The system proxy mainly affects HTTP/HTTPS applications that honor the proxy setting; browser results cannot replace an SSH test. If a research server requires a campus VPN, first satisfy the server's own network requirement, then run the port test and `ssh -vvv`.

```powershell
Test-NetConnection example.edu -Port 22
ssh -vvv username@example.edu
```

若 443 网页访问正常而 22 端口失败，不应去修改 GitHub、浏览器或 Python 环境；优先检查校园 VPN、服务器端口、服务器维护状态和目标路由。

If HTTPS on port 443 works but the SSH port fails, do not start changing GitHub, browser, or Python settings; inspect the campus VPN, server port, server maintenance status, and target route first.

## 一套适合最近这类故障的恢复顺序
## Recovery Sequence for This Recent Failure Pattern

第一步，把 FlClash 恢复到规则模式、系统代理开启、TUN 关闭。第二步，确认国内网站正常。第三步，只测试 GitHub 和目标外部站点。第四步，若外部站点失败，只更换节点并观察连接/请求/日志。第五步，若只有桌面应用失败，临时打开 TUN 做一次对照。第六步，若 TUN 让全网更差，立即关闭并比较路由与 DNS。第七步，SSH 单独使用 `Test-NetConnection` 与 `ssh -vvv` 判断。

First, return FlClash to rule mode with the system proxy enabled and TUN disabled. Second, confirm that ordinary domestic websites work. Third, test only GitHub and the target external site. Fourth, if those sites fail, change only the node and inspect connections, requests, or logs. Fifth, if only a desktop application fails, enable TUN temporarily for one controlled comparison. Sixth, if TUN makes the whole network worse, disable it immediately and compare routes and DNS. Seventh, diagnose SSH separately with `Test-NetConnection` and `ssh -vvv`.

这套顺序的目的不是保证某个客户端一定恢复，而是让每一次失败都能缩小故障层级，避免“什么都重置一遍，最后不知道为什么好了”。

The purpose of this sequence is not to guarantee that one client will recover; it is to make every failed test narrow the fault layer and avoid the pattern of “reset everything and never learn why it started working.”

## 不要做的事
## What Not to Do

不要同时开启全局模式、TUN、修改 DNS、更换节点并重置 Windows 网络；不要因为代理异常就关闭防火墙、证书验证或学校要求的安全组件；不要把节点订阅、服务器地址、完整路由表或账户信息放进公开 Issue。

Do not simultaneously enable global mode, enable TUN, change DNS, switch nodes, and reset Windows networking; do not disable firewalls, certificate validation, or school-required security components because of a proxy failure; and do not post subscription details, server addresses, complete routing tables, or account information in public issues.

## 经验状态说明
## Status of the Observations

“系统代理开、TUN 关时国内正常而外部站点异常”和“开启 TUN 后整体网络进一步恶化”属于实际观察到的故障模式；它们可以帮助确定排障顺序，但不能直接证明某个节点、DNS、TUN 实现或 Windows 组件就是唯一根因。

“Domestic networking is normal with the system proxy on and TUN off while external sites fail,” and “enabling TUN makes the overall network worse” are observed failure patterns. They are useful for choosing a troubleshooting order, but they do not by themselves prove that one node, DNS configuration, TUN implementation, or Windows component is the unique root cause.

## 上游参考
## Upstream Reference

FlClash 项目主页与变更记录可用于确认当前版本是否支持 Windows TUN、系统代理以及连接/请求相关功能。排障手册不固定某个版本号。

The FlClash project page and changelog can be used to confirm whether the current version supports Windows TUN, the system proxy, and connection/request-related features. This playbook does not pin troubleshooting guidance to one version.

- <https://github.com/chen08209/FlClash>
- <https://github.com/chen08209/FlClash/blob/main/CHANGELOG.md>

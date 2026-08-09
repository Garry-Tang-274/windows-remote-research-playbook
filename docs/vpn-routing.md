# VPN、代理与路由排障
# VPN, Proxy, and Routing Troubleshooting

## 先区分 VPN 类型
## First Distinguish the VPN Type

校园访问 VPN、商业代理和应用内代理可能同时存在，但它们的目标和路由规则不同。排障时只保留完成当前任务所需的最少网络层。

A campus-access VPN, commercial proxy, and application-level proxy may coexist, but they have different goals and routing rules. During troubleshooting, keep only the minimum network layers required for the current task.

规则模式通常只代理匹配规则的流量，全局模式通常代理更多流量；具体行为仍取决于客户端规则、DNS、系统代理和 TUN 状态。

Rule mode usually proxies only traffic matching its rules, while global mode usually proxies more traffic; actual behavior still depends on client rules, DNS, the system proxy, and TUN state.

Windows 上使用 FlClash 时，建议同时阅读 [`windows-flclash-routing.md`](windows-flclash-routing.md)。该文档专门处理“系统代理开、TUN 关时网页表现不同”“开启 TUN 后全网变差”“网页正常但桌面应用或 Remote 异常”等情况。

When using FlClash on Windows, also read [`windows-flclash-routing.md`](windows-flclash-routing.md). It focuses on cases where websites behave differently with the system proxy enabled and TUN disabled, enabling TUN degrades the whole network, or the web works while a desktop application or Remote does not.

## 系统代理与 TUN 不是同一层
## System Proxy and TUN Are Different Layers

系统代理主要影响愿意读取 Windows 代理设置的 HTTP/HTTPS 程序；TUN 在更低层接管更多流量。因此浏览器、桌面应用和 SSH 可能同时表现不同。

The system proxy mainly affects HTTP/HTTPS programs that honor Windows proxy settings; TUN captures more traffic at a lower layer. Therefore, browsers, desktop applications, and SSH can behave differently at the same time.

排障时优先从“规则模式 + 系统代理开 + TUN 关”建立基线，再按需要临时启用 TUN 做对照。不要把“某个应用只有开 TUN 才能连接”直接解释成“TUN 必须永久开启”。

For troubleshooting, start from a baseline of rule mode with the system proxy enabled and TUN disabled, then enable TUN temporarily only when a controlled comparison is needed. Do not interpret “one application connects only with TUN enabled” as proof that TUN must remain permanently enabled.

## 建立对照测试
## Establish Controlled Tests

分别记录关闭全部 VPN、只开校园 VPN、只开代理、同时开启时的端口测试和网页访问结果。对于 Windows 代理客户端，还应单独记录 TUN 开与关的差异。

Record port-test and web-access results with all VPNs off, only the campus VPN on, only the proxy on, and both enabled. For Windows proxy clients, also record the difference between TUN enabled and disabled.

一次只改变一个变量。若同时切换节点、DNS、规则、TUN 和浏览器，很难确定哪个变化修复或破坏了连接。

Change only one variable at a time. If the node, DNS, rules, TUN, and browser all change together, it becomes difficult to identify which change fixed or broke the connection.

## DNS 与路由
## DNS and Routing

主机名失败但直接 IP 可达时，优先检查 DNS；两者都失败时，优先检查路由和防火墙。

If the hostname fails but the direct IP is reachable, inspect DNS first; if both fail, inspect routing and firewalls first.

```powershell
Resolve-DnsName example.edu
route print
```

TUN 排障时，可在开启前后分别记录网卡、DNS 和 IPv4 路由，再比较差异。

When troubleshooting TUN, record adapters, DNS, and IPv4 routes before and after enabling it, then compare the differences.

```powershell
Get-NetAdapter | Sort-Object Status, Name
Get-DnsClientServerAddress -AddressFamily IPv4
Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric, InterfaceMetric
```

`route print` 和以上命令可能暴露内部网段、接口名称和网络结构，公开分享前应脱敏。

`route print` and the commands above may expose internal subnets, interface names, and network structure, so redact them before public sharing.

## 常见冲突
## Common Conflicts

浏览器能访问但 SSH 不通，可能是系统代理只影响 HTTP；SSH 能通但学校网页异常，可能是 DNS、证书检查或路由优先级冲突。

If the browser works but SSH does not, the system proxy may affect only HTTP; if SSH works but a school webpage fails, DNS, certificate inspection, or route priority may be conflicting.

国内网站正常而 GitHub 或 ChatGPT 很慢时，如果当前是规则模式、系统代理开、TUN 关，优先检查节点、规则命中、DNS 与代理链路；不要先做 Windows 网络重置。

If domestic websites are normal while GitHub or ChatGPT is very slow under rule mode with the system proxy enabled and TUN disabled, inspect the node, rule matching, DNS, and proxy path before resetting Windows networking.

开启 TUN 后国内外网站都明显变慢、超时或不稳定时，先关闭 TUN 回到基线；如果问题随之消失，应继续检查 TUN 路由、DNS 和虚拟网卡，而不是继续叠加更多网络修改。

If enabling TUN makes both domestic and external websites slow, time out, or become unstable, disable TUN and return to the baseline first; if the problem disappears, continue checking TUN routing, DNS, and the virtual adapter instead of stacking more networking changes.

学校 VPN 连接后不要随意禁用安全软件或证书校验。应优先查阅学校文档或联系管理员确认受支持配置。

Do not casually disable security software or certificate validation after connecting to a school VPN. Prefer school documentation or administrator confirmation of supported configurations.

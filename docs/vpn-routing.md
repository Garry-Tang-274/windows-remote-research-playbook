# VPN、代理与路由排障
# VPN, Proxy, and Routing Troubleshooting

## 先区分 VPN 类型
## First Distinguish the VPN Type

校园访问 VPN、商业代理和应用内代理可能同时存在，但它们的目标和路由规则不同。排障时只保留完成当前任务所需的最少网络层。

A campus-access VPN, commercial proxy, and application-level proxy may coexist, but they have different goals and routing rules. During troubleshooting, keep only the minimum network layers required for the current task.

规则模式通常只代理匹配规则的流量，全局模式通常代理更多流量；具体行为仍取决于客户端规则、DNS 和系统代理设置。

Rule mode usually proxies only traffic matching its rules, while global mode usually proxies more traffic; actual behavior still depends on client rules, DNS, and system proxy settings.

## 建立对照测试
## Establish Controlled Tests

分别记录关闭全部 VPN、只开校园 VPN、只开代理、同时开启时的端口测试和网页访问结果。

Record port-test and web-access results with all VPNs off, only the campus VPN on, only the proxy on, and both enabled.

一次只改变一个变量。若同时切换节点、DNS、规则和浏览器，很难确定哪个变化修复或破坏了连接。

Change only one variable at a time. If the node, DNS, rules, and browser all change together, it becomes difficult to identify which change fixed or broke the connection.

## DNS 与路由
## DNS and Routing

主机名失败但直接 IP 可达时，优先检查 DNS；两者都失败时，优先检查路由和防火墙。

If the hostname fails but the direct IP is reachable, inspect DNS first; if both fail, inspect routing and firewalls first.

```powershell
Resolve-DnsName example.edu
route print
```

`route print` 可能暴露内部网段和接口信息，公开分享前应脱敏。

`route print` may expose internal network ranges and interface information, so redact it before public sharing.

## 常见冲突
## Common Conflicts

浏览器能访问但 SSH 不通，可能是系统代理只影响 HTTP；SSH 能通但学校网页异常，可能是 DNS、证书检查或路由优先级冲突。

If the browser works but SSH does not, the system proxy may affect only HTTP; if SSH works but a school webpage fails, DNS, certificate inspection, or route priority may be conflicting.

学校 VPN 连接后不要随意禁用安全软件或证书校验。应优先查阅学校文档或联系管理员确认受支持配置。

Do not casually disable security software or certificate validation after connecting to a school VPN. Prefer school documentation or administrator confirmation of supported configurations.

# Android Clash 分流与后台存活排障附录
# Android Clash Split-Tunneling and Background Survival Appendix

本附录记录 Android 设备上代理应用的分应用路由、规则模式和后台存活问题。它是移动端网络附录，不改变本仓库以 Windows 远程科研开发为主的范围。

This appendix records per-app routing, rule mode, and background-survival issues for proxy applications on Android devices. It is a mobile-network appendix and does not change the repository’s primary scope of Windows-based remote research development.

本文只讨论用户有权使用的网络和服务，不提供绕过组织安全策略、地区限制或访问控制的方法。

This document discusses only networks and services the user is authorized to use and does not provide methods to bypass organizational security policies, regional restrictions, or access controls.

## 1. 先确认分流模式的语义
## 1. Confirm the Meaning of the Split-Tunneling Mode

“允许所选应用”通常表示只有被勾选应用进入 VPN；“拒绝所选应用”通常表示被勾选应用绕过 VPN，其余应用进入 VPN。

“Allow selected apps” usually means only selected applications use the VPN; “Deny selected apps” usually means selected applications bypass the VPN while all remaining applications use it.

不同客户端的中文翻译可能不一致，因此不要只看选项名称。修改前先用一个需要代理的应用和一个不需要代理的应用做对照测试。

Translations differ across clients, so do not rely on the option label alone. Before changing the configuration, test one application that requires the proxy and one that should bypass it.

如果启用允许列表后，未出现在列表中的应用无法联网或无法稳定发送请求，优先怀疑列表语义或应用遗漏，而不是立刻修改节点、DNS 和规则文件。

If applications omitted from an allowlist cannot connect or send requests reliably, first suspect allowlist semantics or missing applications rather than immediately changing nodes, DNS, and rule files.

## 2. 对大多数日常场景优先使用拒绝列表
## 2. Prefer a Denylist for Most Daily-Use Scenarios

当目标是“绝大多数海外服务走代理，少数本地高敏感应用直连”时，拒绝列表通常比允许列表更稳健。

When the goal is “most overseas services use the proxy while a small number of sensitive local applications connect directly,” a denylist is usually more robust than an allowlist.

把支付、银行、运营商和仅限本地网络的应用加入绕过列表，其余应用保留走 VPN，可以减少新安装应用因未加入允许列表而完全失联的风险。

Add payment, banking, carrier, and local-network-only applications to the bypass list while allowing the remaining applications to use the VPN; this reduces the risk that newly installed applications lose connectivity because they were omitted from an allowlist.

不要公开截图中的完整应用清单，因为它可能暴露金融应用、学校系统、工作应用或个人使用习惯。

Do not publish screenshots containing the complete application list because it may reveal financial applications, institutional systems, work applications, or personal usage habits.

## 3. 规则模式与分应用路由是两个层级
## 3. Rule Mode and Per-App Routing Are Separate Layers

分应用路由决定应用是否进入 VPN；规则模式决定进入 VPN 后的具体流量是代理、直连还是拒绝。

Per-app routing determines whether an application enters the VPN; rule mode determines whether traffic that entered the VPN is proxied, connected directly, or rejected.

应用被正确纳入 VPN 后仍无法使用时，再检查规则命中、域名解析、节点可用性和协议兼容性。

If an application is correctly included in the VPN but still fails, then inspect rule matching, DNS resolution, node availability, and protocol compatibility.

排障时一次只改变一个层级。先固定节点和规则模式，只测试分应用列表；确认后再修改 DNS 或规则。

Change only one layer at a time during troubleshooting. First keep the node and rule mode fixed while testing the per-app list; modify DNS or rules only after that layer is verified.

## 4. 应用列表可能不完整
## 4. The Application List May Be Incomplete

某些系统组件、商店、WebView、登录服务或共享进程可能不会以直观名称出现在应用列表中。

Some system components, app stores, WebView processes, login services, or shared processes may not appear under intuitive names in the application list.

列表中找不到某个应用，不代表它不受 VPN 影响。它可能通过系统服务、共享 UID 或浏览器组件发起请求。

An application being absent from the list does not mean it is unaffected by the VPN. It may send requests through a system service, shared UID, or browser component.

遇到登录页、凭据选择器或商店无法加载时，应同时测试浏览器、系统 WebView、Google Play 服务或相应系统组件，而不是只测试主应用。

When a login page, credential chooser, or app store fails to load, test the browser, system WebView, Google Play services, or relevant system component in addition to the main application.

## 5. 修改分流后必须重启 VPN 会话
## 5. Restart the VPN Session After Routing Changes

部分客户端不会把新的分应用设置即时应用到现有 VPN 会话。修改后应停止并重新启动 VPN，再重新打开目标应用。

Some clients do not apply new per-app settings immediately to an existing VPN session. After modifying the list, stop and restart the VPN, then reopen the target application.

仅从最近任务中划掉应用可能不够，因为应用进程、DNS 缓存和长连接仍可能保留旧状态。

Removing an application from recent tasks may be insufficient because application processes, DNS caches, and persistent connections may retain the old state.

必要时依次执行：重启 VPN、强制停止目标应用、重新打开应用；不要一开始就清除应用数据或重新安装。

When necessary, restart the VPN, force-stop the target application, and reopen it in that order; do not begin by clearing application data or reinstalling the app.

## 6. 始终开启 VPN 与后台限制是两个问题
## 6. Always-On VPN and Background Restrictions Are Separate Issues

关闭 Android 的“始终开启 VPN”通常会立即结束系统维护的当前 VPN 会话，而不仅仅是取消下次自动连接。

Turning off Android’s “Always-on VPN” usually ends the currently system-maintained VPN session immediately rather than merely disabling future automatic connection.

关闭始终开启后，代理应用仍可能在前台正常运行，但系统的电池优化、智能后台限制或厂商清理策略可能稍后终止它。

After Always-on VPN is disabled, the proxy application may continue working in the foreground, but battery optimization, adaptive background restrictions, or vendor cleanup policies may terminate it later.

需要即时可用和稳定后台连接时，应允许后台运行并考虑始终开启；更重视电量时，可以手动启动，但必须接受后台被杀后需要重新连接。

When immediate availability and stable background connectivity are required, allow background operation and consider Always-on VPN; when battery life is more important, manual startup is possible but requires accepting reconnection after the process is killed.

## 7. 最小排障顺序
## 7. Minimal Troubleshooting Order

第一步确认 VPN 会话是否存在；第二步确认目标应用是否进入 VPN；第三步确认规则模式与节点；第四步检查 DNS 和系统组件；最后才考虑重装或清除数据。

First confirm that the VPN session exists; second confirm that the target application enters the VPN; third confirm rule mode and node availability; fourth inspect DNS and system components; only then consider reinstalling or clearing data.

每一步都应记录“修改前现象、唯一改动、修改后结果”。如果同时切换模式、节点、DNS 和后台权限，就无法确定根因。

For each step, record the symptom before the change, the single modification, and the result afterward. If mode, node, DNS, and background permission are changed simultaneously, the root cause cannot be determined.

## 8. 已确认经验与未确认推测分开记录
## 8. Separate Confirmed Findings from Unverified Hypotheses

只有在切换分流模式后问题可重复消失，并在恢复旧模式后可重复出现时，才能把分流模式写成已确认根因。

Treat split-tunneling mode as a confirmed root cause only when the issue reproducibly disappears after changing the mode and reappears after restoring the old mode.

应用列表缺失、凭据管理器状态或系统服务参与等情况，如果没有日志或可重复对照，应写成合理推测而不是确定结论。

When application-list omissions, credential-manager state, or system-service involvement lack logs or reproducible controls, record them as reasonable hypotheses rather than confirmed conclusions.

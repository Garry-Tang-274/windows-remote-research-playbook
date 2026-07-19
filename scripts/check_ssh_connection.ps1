[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$HostName,
    [int]$Port = 22
)

$ErrorActionPreference = 'Continue'
Write-Host "[信息] 测试 TCP 连接：$HostName`:$Port"
Write-Host "[INFO] Testing TCP connectivity: $HostName`:$Port"
$result = Test-NetConnection -ComputerName $HostName -Port $Port -InformationLevel Detailed
$result | Select-Object ComputerName, RemoteAddress, RemotePort, NameResolutionSucceeded, TcpTestSucceeded

if ($result.TcpTestSucceeded) {
    Write-Host "[通过] 目标端口可达。下一步可在 PowerShell 中运行 ssh -vvv。"
    Write-Host "[PASS] The target port is reachable. Next, run ssh -vvv in PowerShell."
    exit 0
}

Write-Host "[失败] 目标端口不可达。优先检查 VPN、路由、防火墙、端口和服务器状态。"
Write-Host "[FAIL] The target port is unreachable. Check VPN, routing, firewall, port, and server status first."
exit 1

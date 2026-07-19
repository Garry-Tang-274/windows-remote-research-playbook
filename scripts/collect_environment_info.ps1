[CmdletBinding()]
param(
    [string]$OutputPath = ".\environment_summary.txt"
)

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("Windows 远程科研环境摘要 / Windows Remote Research Environment Summary")
$lines.Add("生成时间 / Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')")
$lines.Add("")
$lines.Add("操作系统 / Operating system:")
$lines.Add((Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture | Format-List | Out-String).Trim())
$lines.Add("")
$lines.Add("PowerShell:")
$lines.Add($PSVersionTable.PSVersion.ToString())
$lines.Add("")
$lines.Add("OpenSSH:")
$ssh = Get-Command ssh -ErrorAction SilentlyContinue
$lines.Add($(if ($ssh) { $ssh.Source } else { "未找到 / Not found" }))
$lines.Add("")
$lines.Add("Python 启动器 / Python launchers:")
foreach ($command in @('py', 'python', 'python3')) {
    $item = Get-Command $command -ErrorAction SilentlyContinue
    $lines.Add("$command: $(if ($item) { $item.Source } else { '未找到 / Not found' })")
}
$lines.Add("")
$lines.Add("说明：本文件不收集密码、令牌、Cookie 或 SSH 私钥。")
$lines.Add("Note: This file does not collect passwords, tokens, cookies, or SSH private keys.")

$lines | Set-Content -Path $OutputPath -Encoding UTF8
Write-Host "[完成] 已写入：$OutputPath"
Write-Host "[DONE] Written to: $OutputPath"

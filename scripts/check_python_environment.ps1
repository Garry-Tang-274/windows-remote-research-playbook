$ErrorActionPreference = 'Continue'
Write-Host "[信息] 检查 Python 解释器与包管理器。"
Write-Host "[INFO] Inspecting Python interpreters and package managers."

Write-Host "`nwhere.exe python"
where.exe python 2>$null
Write-Host "`nwhere.exe py"
where.exe py 2>$null

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "`n[信息] 当前 python 版本与路径："
    Write-Host "[INFO] Current python version and path:"
    python --version
    python -c "import sys; print(sys.executable); print('prefix=', sys.prefix); print('base_prefix=', sys.base_prefix)"
    python -m pip --version
} else {
    Write-Host "[警告] 当前 PATH 中没有 python。"
    Write-Host "[WARN] No python command is available on the current PATH."
}

Write-Host "`n[提示] 安装包时优先使用 python -m pip。"
Write-Host "[TIP] Prefer python -m pip when installing packages."

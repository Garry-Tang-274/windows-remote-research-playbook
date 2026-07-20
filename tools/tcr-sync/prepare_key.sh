#!/usr/bin/env bash
set -euo pipefail

# Create a repository-specific SSH deploy key. / 创建仅用于目标仓库的 SSH Deploy Key。
KEY_DIR="${HOME}/.ssh"
KEY_FILE="${KEY_DIR}/id_ed25519_tcr_sync"
mkdir -p "$KEY_DIR"
chmod 700 "$KEY_DIR"

if [[ -f "$KEY_FILE" && -f "${KEY_FILE}.pub" ]]; then
  echo "Existing TCR sync key detected. / 检测到已有 TCR 同步密钥。"
else
  ssh-keygen -t ed25519 -C "tcr-sync-deploy-key" -f "$KEY_FILE" -N ""
fi

chmod 600 "$KEY_FILE"
chmod 644 "${KEY_FILE}.pub"
echo
echo "Copy the entire public-key line below. / 复制下面完整的一行公钥。"
echo "----------------------------------------------------------------"
cat "${KEY_FILE}.pub"
echo "----------------------------------------------------------------"
echo "Create the private repository tcr-pairing-research-sync, add this key under Settings → Deploy keys, enable Allow write access, then run bash install.sh."
echo "新建私有仓库 tcr-pairing-research-sync，在 Settings → Deploy keys 中添加此公钥并勾选 Allow write access，然后运行 bash install.sh。"

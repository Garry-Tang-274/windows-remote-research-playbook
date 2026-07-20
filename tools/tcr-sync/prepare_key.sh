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
echo
echo "GitHub steps / GitHub 操作："
echo "1. Create an empty private repository named tcr-pairing-research-sync."
echo "   新建名为 tcr-pairing-research-sync 的空白私有仓库。"
echo "2. Open Settings → Deploy keys → Add deploy key."
echo "   打开 Settings → Deploy keys → Add deploy key。"
echo "3. Paste the key and enable Allow write access."
echo "   粘贴公钥，并勾选 Allow write access。"
echo "4. Return here and run: bash install.sh"
echo "   回到这里运行：bash install.sh"

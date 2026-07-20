#!/usr/bin/env bash
set -euo pipefail

# Install the TCR synchronization workflow for the known server project.
# 为已知服务器项目安装 TCR 自动同步流程。
TOOL_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="/mnt/volume3/TangZhi_TCR_Embedding_Project"
REPO_SSH_URL="git@github.com:Garry-Tang-274/tcr-pairing-research-sync.git"
MIRROR_DIR="${HOME}/tcr-pairing-research-sync"
CONFIG_DIR="${HOME}/.config/tcr-sync"
SHARE_DIR="${HOME}/.local/share/tcr-sync"
BIN_DIR="${HOME}/.local/bin"
STATE_DIR="${HOME}/.local/state/tcr-sync"
KEY_FILE="${HOME}/.ssh/id_ed25519_tcr_sync"

for command_name in git python3 rsync ssh crontab; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing command: $command_name / 缺少命令：$command_name"
    exit 1
  fi
done

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "TCR project directory not found: $SOURCE_DIR"
  echo "未找到 TCR 项目目录：$SOURCE_DIR"
  exit 1
fi

if [[ ! -f "$KEY_FILE" ]]; then
  echo "Deploy key not found. Run: bash prepare_key.sh"
  echo "未找到 Deploy Key。请运行：bash prepare_key.sh"
  exit 1
fi

mkdir -p "$CONFIG_DIR" "$SHARE_DIR" "$BIN_DIR" "$STATE_DIR"

export GIT_SSH_COMMAND="ssh -i ${KEY_FILE} -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

echo "Testing private repository access. / 正在测试私有仓库访问。"
if ! git ls-remote "$REPO_SSH_URL" >/dev/null; then
  echo "Cannot access the private repository. / 无法访问私有仓库。"
  echo "Confirm the repository exists and the deploy key has write access."
  echo "请确认仓库已建立，并且 Deploy Key 已启用写入权限。"
  exit 1
fi

if [[ -d "$MIRROR_DIR/.git" ]]; then
  echo "Existing mirror detected: $MIRROR_DIR / 检测到已有镜像：$MIRROR_DIR"
else
  if [[ -e "$MIRROR_DIR" && -n "$(ls -A "$MIRROR_DIR" 2>/dev/null)" ]]; then
    echo "Mirror path exists and is not empty: $MIRROR_DIR"
    echo "镜像路径已存在且非空：$MIRROR_DIR"
    exit 1
  fi
  git clone "$REPO_SSH_URL" "$MIRROR_DIR"
fi

cp "$TOOL_DIR/include.list" "$CONFIG_DIR/include.list"
cp "$TOOL_DIR/exclude.list" "$CONFIG_DIR/exclude.list"
cp "$TOOL_DIR/build_manifest.py" "$SHARE_DIR/build_manifest.py"
cp "$TOOL_DIR/tcr-sync" "$BIN_DIR/tcr-sync"
chmod 700 "$SHARE_DIR/build_manifest.py" "$BIN_DIR/tcr-sync"

cat > "$CONFIG_DIR/sync.env" <<EOF_CONFIG
SOURCE_DIR="$SOURCE_DIR"
MIRROR_DIR="$MIRROR_DIR"
REPO_SSH_URL="$REPO_SSH_URL"
GIT_BRANCH="main"
MAX_FILE_MIB="50"
GIT_AUTHOR_NAME="TCR Sync Bot"
GIT_AUTHOR_EMAIL="tcr-sync@localhost"
EOF_CONFIG
chmod 600 "$CONFIG_DIR/sync.env"

if [[ ! -f "$MIRROR_DIR/.gitignore" ]]; then
  cat > "$MIRROR_DIR/.gitignore" <<'EOF_GITIGNORE'
# Secrets and local state / 密钥与本地状态
.env
.env.*
*.pem
*.key
*.p12
*.pfx
__pycache__/
.pytest_cache/
.mypy_cache/
.ipynb_checkpoints/
.cache/
tmp/
temp/

# Large research artifacts / 大型科研产物
raw_data/
processed_data/
embeddings/
checkpoints/
models/
wandb/
mlruns/
*.pt
*.pth
*.ckpt
*.onnx
*.npy
*.npz
*.h5
*.hdf5
*.tar
*.tar.gz
*.tgz
*.zip
*.7z
*.rar
EOF_GITIGNORE
fi

# Replace only the cron line managed by this installer. / 只替换由本安装器管理的 cron 行。
temporary_cron="$(mktemp)"
trap 'rm -f "$temporary_cron"' EXIT
{
  (crontab -l 2>/dev/null || true) | grep -v '# tcr-sync-managed' || true
} > "$temporary_cron"
printf '17 */6 * * * %s >> %s 2>&1 # tcr-sync-managed\n' \
  "$BIN_DIR/tcr-sync" "$STATE_DIR/cron.log" >> "$temporary_cron"
crontab "$temporary_cron"

echo "Running the first synchronization. / 正在执行首次同步。"
"$BIN_DIR/tcr-sync"

echo
echo "Installation completed. / 安装完成。"
echo "Manual sync / 手动同步：$BIN_DIR/tcr-sync"
echo "Log / 日志：$STATE_DIR/sync.log"
echo "Whitelist / 白名单：$CONFIG_DIR/include.list"
echo "Schedule / 定时：every six hours / 每六小时一次"

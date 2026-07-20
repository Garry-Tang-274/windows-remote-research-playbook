# TCR Server Auto-Sync / TCR 服务器自动同步

This installer deploys a zero-extra-cost synchronization workflow for the TCR project server. It uses Git, SSH, rsync, Python, and cron only; it does not call a paid AI API.

本安装器为 TCR 项目服务器部署零额外付费的自动同步流程。它只使用 Git、SSH、rsync、Python 和 cron，不调用任何付费 AI API。

## What it synchronizes / 同步内容

Only paths explicitly listed in `include.list` are copied. Large files, raw data, embeddings, model checkpoints, archives, caches, environment files, keys, and tokens are excluded by default.

只复制 `include.list` 中明确列出的路径。大文件、原始数据、embedding、模型检查点、压缩包、缓存、环境文件、密钥和令牌默认全部排除。

The default source directory is `/mnt/volume3/TangZhi_TCR_Embedding_Project`. The default destination repository is the private repository `Garry-Tang-274/tcr-pairing-research-sync`.

默认源目录是 `/mnt/volume3/TangZhi_TCR_Embedding_Project`。默认目标仓库是私有仓库 `Garry-Tang-274/tcr-pairing-research-sync`。

## Deployment order / 部署顺序

First clone this public toolkit repository on the server and generate a repository-specific deploy key:

首先在服务器克隆这个公共工具仓库，并生成仅用于目标仓库的 Deploy Key：

```bash
git clone --depth 1 https://github.com/Garry-Tang-274/windows-remote-research-playbook.git ~/windows-remote-research-playbook && cd ~/windows-remote-research-playbook/tools/tcr-sync && bash prepare_key.sh
```

Create an empty private GitHub repository named `tcr-pairing-research-sync`. Do not initialize a README, `.gitignore`, or license. Add the printed public key under `Settings → Deploy keys → Add deploy key`, and enable `Allow write access`.

在 GitHub 新建名为 `tcr-pairing-research-sync` 的空白私有仓库，不初始化 README、`.gitignore` 或许可证。把终端显示的公钥添加到 `Settings → Deploy keys → Add deploy key`，并启用 `Allow write access`。

Then return to the server and run:

然后回到服务器运行：

```bash
cd ~/windows-remote-research-playbook/tools/tcr-sync && bash install.sh
```

The installer validates the source directory and GitHub SSH access, creates a local mirror, installs the sync command, registers a six-hour cron schedule, and performs the first synchronization.

安装器会验证源目录和 GitHub SSH 访问，建立本地镜像，安装同步命令，注册每六小时运行一次的 cron 任务，并执行首次同步。

## Daily use / 日常使用

```bash
~/.local/bin/tcr-sync
tail -n 100 ~/.local/state/tcr-sync/sync.log
nano ~/.config/tcr-sync/include.list
```

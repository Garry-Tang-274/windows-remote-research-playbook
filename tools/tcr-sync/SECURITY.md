# Security Notes / 安全说明

This workflow uses an explicit upload whitelist and a separate exclusion list. It does not upload paths outside the whitelist.

本流程使用明确的上传白名单和独立排除规则，不会上传白名单以外的路径。

The server stores a repository-specific deploy key at `~/.ssh/id_ed25519_tcr_sync`. The private key must never be copied into the project directory or committed to Git.

服务器会在 `~/.ssh/id_ed25519_tcr_sync` 保存仅用于目标仓库的 Deploy Key。私钥不得复制到项目目录，也不得提交到 Git。

The destination repository must remain private unless the research group explicitly approves publication.

除非研究组明确批准公开，目标仓库必须保持为私有仓库。

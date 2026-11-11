# 完整检查后再发布
# Publish a Complete, Checked Change

把同一功能的程序、调用方、测试、配置模板和说明放在同一次提交中。逐文件向默认分支写入，会让中间状态触发重复失败；关闭所有通知并不能修复这些中间状态。

Commit a feature's code, callers, tests, example configuration and documentation together. File-by-file writes to the default branch expose incomplete states and can trigger repeated failures; disabling all notifications does not repair those states.

## 发布前
## Before Pushing

读取最新默认分支和当前改动，只暂存本次有意发布的文件。运行项目已有的检查；新增文件同时补齐索引、示例及调用入口。检查失败就在本地修复，不靠重复推送碰运气。

Read the latest default branch and current changes, then stage only intended files. Run the project's existing checks and complete indexes, examples and entry points for new files. Repair failures locally rather than repeatedly pushing unchanged errors.

```powershell
git status --short
git diff --check
git diff --cached --stat
```

这些命令只查看状态和差异，不修改系统或需要管理员权限。后续暂存、提交和推送会修改仓库，执行前应确认完整内容；已发布后的恢复通常通过新的 revert 提交，而不是强制覆盖共享历史。

These commands inspect state and differences; they do not change system settings or require administrator privileges. Staging, committing and pushing modify the repository, so inspect the complete content first. Restore published changes with a new revert commit rather than overwriting shared history.

## 发生并发更新时
## When Another Writer Publishes

重新获取默认分支，保留并合并他人的提交，再检查实际合并结果。Pull Request 检查通过后，如果目标分支又发生变化，原有检查不自动证明最终合并树仍然正确；发布后仍需查看该提交的结果。

Fetch the default branch again, preserve and merge the other writer's commits, then check the merged result. If the target changes after a pull-request check, that earlier check does not establish the final merged tree's correctness; inspect the actual published commit's checks.

## 本地钩子与服务器保护不同
## Local Hooks and Server Protection Differ

本地 `pre-push` 只对安装了它的副本生效，网页和 API 写入不经过该钩子。需要服务器强制检查时核对当前套餐和仓库权限；不要未经授权公开私有仓库、改变访问权限或购买套餐。

A local `pre-push` hook applies only to checkouts where it is installed; web and API writes bypass it. Check current plan and repository permissions before relying on server-enforced checks. Do not make a private repository public, change access or buy a plan without authorization.

敏感配置、会话、下载、诊断日志、私人相册和受限课件不属于公开源码包。新建仓库应先明确哪些内容可以公开，再创建仓库并读回关键文件与可见性。

Private configuration, sessions, downloads, diagnostic logs, private photo collections and restricted course materials do not belong in a public source package. Define the publishable contents before repository creation, then verify key files and visibility after publishing.

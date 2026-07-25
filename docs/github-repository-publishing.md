# GitHub 仓库发布与连接器排障
# GitHub Repository Publishing and Connector Troubleshooting

本章总结如何把本地或临时环境中的项目可靠地发布到 GitHub，并处理“连接器可以读取仓库但不能完成某些操作”“提交已经产生但文件没有完整出现”“GitHub Actions 没有按预期运行”等问题。

This chapter explains how to publish projects from a local or temporary environment to GitHub reliably and how to handle cases where a connector can read repositories but cannot perform certain operations, commits exist but files are incomplete, or GitHub Actions do not run as expected.

## 先区分三种操作环境
## Distinguish the Three Operating Environments First

GitHub 网页、GitHub App 或连接器、以及本机的 `git` 与 GitHub CLI 是三个不同的操作环境。它们可能连接同一个账号，但权限范围、可调用接口和认证方式并不相同。

The GitHub website, a GitHub App or connector, and local `git` plus GitHub CLI are three different operating environments. They may connect to the same account, but their permission scopes, available operations, and authentication methods are different.

连接器能够列出、读取和写入已有仓库，不代表它一定能够创建新仓库、修改仓库设置、触发工作流或上传任意大小与类型的文件。

A connector being able to list, read, and write existing repositories does not guarantee that it can create repositories, change repository settings, trigger workflows, or upload files of any size and type.

本机 `git` 适合完整目录、二进制文件、大量文件和可审计的提交历史；GitHub CLI 适合认证检查、仓库创建、Pull Request 和 Actions 日志；连接器适合结构化读取以及少量文本文件修改。

Local `git` is suitable for complete directories, binary files, large file sets, and auditable commit history; GitHub CLI is suitable for authentication checks, repository creation, pull requests, and Actions logs; connectors are suitable for structured reading and small text-file modifications.

## 情况一：连接器无法创建仓库
## Case 1: The Connector Cannot Create a Repository

症状是连接器能够识别账号并列出已有仓库，但工具列表中没有创建仓库的操作，或创建操作返回权限错误。

The symptom is that the connector can identify the account and list existing repositories, but no repository-creation action is available, or the action returns a permission error.

这通常不是账号本身没有权限，而是 GitHub App 的安装权限或连接器暴露的接口范围不包含仓库创建。

This usually does not mean that the account lacks permission; it means that the GitHub App installation or the connector's exposed interface does not include repository creation.

最稳妥的处理方式是在 GitHub 网页创建空仓库，或在已登录的本机终端执行以下命令。

The most reliable solution is to create an empty repository on the GitHub website or run the following command in an authenticated local terminal.

```powershell

gh auth status
gh repo create OWNER/REPOSITORY --public --confirm
```

创建用于程序化写入的空仓库时，不要同时初始化 README、`.gitignore` 或许可证，否则后续推送本地已有历史时可能产生不必要的分支分歧。

When creating an empty repository for programmatic writing, do not initialize a README, `.gitignore`, or license at the same time, because doing so may create unnecessary branch divergence when pushing an existing local history.

如果准备直接在 GitHub 网页或连接器中逐个创建文件，则初始化 README 并不会造成技术错误，但应事先统一工作流，避免一部分文件来自本地提交、另一部分来自网页提交。

If files will be created individually through the GitHub website or connector, initializing a README is not technically incorrect, but the workflow should be decided in advance to avoid mixing local commits and web-created commits unintentionally.

## 情况二：少量文件与大量文件使用了同一种写入方式
## Case 2: Small and Large File Sets Use the Same Write Method

GitHub Contents API 适合新建或更新少量 UTF-8 文本文件。每次调用通常产生一个提交，因此用它上传几十个文件会造成提交历史碎片化，也更容易在中途失败。

The GitHub Contents API is suitable for creating or updating a small number of UTF-8 text files. Each call usually creates one commit, so using it for dozens of files fragments the commit history and increases the chance of partial failure.

少量文件可以使用 `create_file` 或 `update_file`；大量文本文件更适合通过 Git Tree 一次性提交，或使用本机 `git add`、`git commit` 和 `git push`。

A small number of files can use `create_file` or `update_file`; a large text-file set is better submitted through a single Git Tree commit or with local `git add`, `git commit`, and `git push`.

Git Tree 工作流通常由四步组成：创建 blob、创建 tree、创建 commit、移动分支引用。任一步失败都不应移动默认分支。

A Git Tree workflow usually consists of four steps: create blobs, create a tree, create a commit, and move the branch reference. The default branch should not be moved if any preceding step fails.

```text
create_blob → create_tree → create_commit → update_ref
```

对完整项目目录，优先使用本机 Git 工作流，因为它能保留文件权限、处理二进制文件、运行本地检查，并在推送前查看完整差异。

For a complete project directory, prefer the local Git workflow because it preserves file modes, handles binary files, allows local validation, and shows the complete diff before pushing.

```powershell

git status --short
git add README.md docs scripts
git diff --cached --stat
git commit -m "Add complete bilingual project files"
git push -u origin main
```

不要在没有检查工作区的情况下使用 `git add -A`，否则可能把日志、密钥、数据文件或无关修改一并上传。

Do not use `git add -A` without inspecting the working tree, because logs, secrets, data files, or unrelated changes may be uploaded unintentionally.

## 情况三：提交已经出现，但项目仍不完整
## Case 3: Commits Exist but the Project Is Still Incomplete

看到提交 SHA 只能证明某次写操作成功，不能证明完整项目已经到达默认分支。

Seeing a commit SHA proves only that one write operation succeeded; it does not prove that the complete project reached the default branch.

常见问题包括：只有 README 被写入、上传在某个临时分支、默认分支引用没有更新、中间分片文件仍存在、某次写入被拦截、或者最后一个清理步骤没有执行。

Common problems include only the README being written, files being uploaded to a temporary branch, the default branch reference not being updated, intermediate fragment files remaining, one write being blocked, or the final cleanup step not running.

发布完成后至少检查以下内容：仓库默认分支、最终提交信息、README、一个深层目录文件、一个关键脚本，以及临时文件是否消失。

After publishing, check at least the repository's default branch, final commit message, README, one deeply nested file, one key script, and whether temporary files have disappeared.

```powershell

gh repo view OWNER/REPOSITORY --json defaultBranchRef,url
gh api repos/OWNER/REPOSITORY/commits/main --jq '.sha, .commit.message'
gh api repos/OWNER/REPOSITORY/contents/README.md --jq '.sha'
gh api repos/OWNER/REPOSITORY/contents/docs/example.md --jq '.sha'
```

通过连接器发布时，也应再次读取关键文件，而不是只依赖写入工具返回的成功状态。

When publishing through a connector, read the key files again instead of relying only on the success status returned by the write action.

## 情况四：GitHub Actions 没有按预期运行
## Case 4: GitHub Actions Do Not Run as Expected

工作流文件已经进入 `.github/workflows/`，但没有出现运行记录时，先不要反复修改业务文件来“碰运气”触发。

If a workflow file exists under `.github/workflows/` but no run appears, do not repeatedly modify project files merely to try to trigger it.

先检查工作流 YAML 是否有效、触发条件是否匹配当前事件、Actions 是否在仓库设置中启用、工作流是否位于默认分支，以及提交是否由某些不会再次触发工作流的自动化身份产生。

First check whether the workflow YAML is valid, whether the trigger matches the current event, whether Actions are enabled in repository settings, whether the workflow is on the default branch, and whether the commit was produced by an automation identity that does not trigger another workflow.

```powershell

gh workflow list --repo OWNER/REPOSITORY
gh run list --repo OWNER/REPOSITORY --limit 10
gh api repos/OWNER/REPOSITORY/actions/permissions
```

某些 GitHub App、自动化令牌或由工作流自身产生的提交可能受到防止递归触发的限制。具体行为取决于认证身份、令牌类型、仓库权限和事件类型，不能仅凭“文件已经 push”判断工作流一定会运行。

Some GitHub Apps, automation tokens, or commits produced by workflows themselves may be subject to recursion-prevention restrictions. The exact behavior depends on the authenticated identity, token type, repository permissions, and event type; a pushed file alone does not guarantee that a workflow will run.

需要可靠触发时，优先使用显式的 `workflow_dispatch`，并从 GitHub 网页或已认证的 GitHub CLI 手动运行。

When reliable triggering is required, prefer an explicit `workflow_dispatch` trigger and start it manually from the GitHub website or an authenticated GitHub CLI session.

```yaml
on:
  workflow_dispatch:
```

```powershell

gh workflow run WORKFLOW_FILE.yml --repo OWNER/REPOSITORY
gh run watch --repo OWNER/REPOSITORY
```

如果工作流只用于一次性恢复文件，恢复完成后应删除该工作流，避免未来无意触发或给读者造成错误印象。

If a workflow is used only for one-time file restoration, delete it after restoration to prevent accidental future runs or misleading readers about the repository's normal architecture.

## 情况五：临时分片与恢复脚本残留
## Case 5: Temporary Fragments and Bootstrap Scripts Remain

通过受限接口传输大文本时，可能需要把内容拆成多个临时分片。分片只应作为传输手段，不应成为项目正式结构的一部分。

When large text is transferred through a constrained interface, it may need to be divided into temporary fragments. Fragments should remain a transport mechanism and must not become part of the project's permanent structure.

恢复成功后应删除分片、一次性工作流、临时清单和包含恢复载荷的脚本，并确认默认分支只保留用户真正需要的源码和文档。

After restoration succeeds, delete fragments, one-time workflows, temporary manifests, and scripts containing restoration payloads, then confirm that the default branch contains only the source code and documentation users actually need.

在清理前先读取最终文件并校验数量或哈希；不要先删除唯一的恢复来源，再检查目标文件是否完整。

Before cleanup, read the final files and verify their count or hashes; do not delete the only restoration source before confirming that the target files are complete.

## 推荐发布决策
## Recommended Publishing Decision

文件少于约五个且均为短文本时，可以使用连接器或 Contents API 直接写入。

When there are fewer than roughly five files and all are short text, direct writing through a connector or the Contents API is reasonable.

文件较多但均为文本，且环境无法使用本机 Git 时，可以使用 Git Tree 生成一个完整提交。

When there are many files but all are text and local Git is unavailable, use a Git Tree to create one complete commit.

项目包含二进制资源、大文件、文件权限、符号链接或需要本地测试时，应使用本机 Git；超出 GitHub 普通文件限制的资源应评估 Git LFS 或外部发布渠道。

When the project contains binary assets, large files, file permissions, symbolic links, or requires local testing, use local Git; assets beyond GitHub's normal file limits should be evaluated for Git LFS or an external release channel.

仓库创建、分支保护、Secrets、Actions 权限和 Pages 设置属于仓库级配置，优先通过 GitHub 网页或 GitHub CLI 明确完成，不要假设文件写入连接器同时具有这些权限。

Repository creation, branch protection, secrets, Actions permissions, and Pages settings are repository-level configuration. Configure them explicitly through the GitHub website or GitHub CLI rather than assuming that a file-writing connector also has those permissions.

## 最终验收清单
## Final Acceptance Checklist

- 仓库名称、Description、可见性和 Topics 正确。
- Repository name, description, visibility, and topics are correct.
- 默认分支与预期一致。
- The default branch matches the intended branch.
- README 能正确显示，且链接没有失效。
- The README renders correctly and contains no broken links.
- 至少一个深层目录文件和一个关键脚本可读取。
- At least one deeply nested file and one key script can be read.
- 临时分片、恢复载荷和一次性工作流已经删除。
- Temporary fragments, restoration payloads, and one-time workflows have been deleted.
- 公开仓库中不存在服务器地址、账号、令牌、密钥、真实研究数据或受版权保护材料。
- The public repository contains no server addresses, accounts, tokens, keys, real research data, or copyrighted materials.
- 最终提交信息能准确描述完整变更，而不是只描述某个中间步骤。
- The final commit message accurately describes the complete change rather than an intermediate step.

## 本章适用边界
## Scope of This Chapter

本章处理的是获得授权的仓库发布与维护，不涉及绕过组织策略、分支保护、访问控制或 GitHub 安全限制。

This chapter covers authorized repository publishing and maintenance. It does not cover bypassing organizational policies, branch protection, access controls, or GitHub security restrictions.

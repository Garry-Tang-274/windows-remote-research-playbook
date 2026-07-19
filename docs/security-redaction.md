# 安全与脱敏
# Security and Redaction

## 必须隐藏的信息
## Information That Must Be Hidden

公开截图或日志前隐藏真实姓名、学校邮箱、个人邮箱、服务器地址、IP、用户名、目录、研究数据文件名、令牌、Cookie、会话 ID、私钥和恢复码。

Before sharing screenshots or logs publicly, hide real names, school and personal email addresses, server addresses, IPs, usernames, directories, research-data filenames, tokens, cookies, session IDs, private keys, and recovery codes.

## 可以保留的信息
## Information That Can Usually Remain

操作系统大版本、软件版本、通用错误码、已脱敏命令结构和不含内部名称的最小复现通常可以保留。

Operating-system major versions, software versions, generic error codes, redacted command structures, and minimal reproductions without internal names can usually remain.

## 脱敏原则
## Redaction Principle

优先复制文本后替换敏感字段，而不是只在截图上画半透明色块；确认元数据和文件名也不暴露信息。

Prefer copying text and replacing sensitive fields rather than drawing translucent blocks on screenshots; also confirm that metadata and filenames reveal nothing sensitive.

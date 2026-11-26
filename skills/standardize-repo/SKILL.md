---
name: standardize-repo
description: 按 standard-repo 规范迁移现有项目目录，或在用户只想评估改动时提供只读方案。
---

# 整理一个仓库

读取同一版本的[仓库整理流程](../../docs/migration.md)，按用户给出的路径、模式和范围执行，用中文报告。相对链接从本文件的真实位置解析；单独载入本文件时，需要同时提供可访问的规范仓库。

可直接用自然语言说明请求。沿用参数写法时使用：

`[项目路径] [--plan] [--type auto|software|ros|assets|dataset|content|research|workspace]`

- 路径省略时使用当前目录，带空格的路径用引号。遇到多个目标、无效路径、未知参数或冲突的类型时先报告问题。
- `--plan` 和“只读盘点”均使用流程中的只读模式。`--type` 采用[选型表](../../docs/repository-types.md)的名称，默认 `auto`。
- 用户明确要求整理或迁移时，在指定范围内实施。本技能以规范仓库自身为目标时只做盘点。

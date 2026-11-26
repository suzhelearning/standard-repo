---
name: standardize-repo
description: 按 standard-repo v2.0 规范盘点或迁移项目目录，识别 Slop 隐患并建立最小确定性护栏。
---

# 整理一个仓库

读取同一版本的[仓库修剪与迁移流程](../../docs/migration.md)，配合[仓库类型与边界契约](../../docs/repository-types.md)和[Feature Map 与确定性护栏](../../docs/verification.md)，按用户给出的路径、模式和范围执行，用中文报告。相对链接从本文件的真实位置解析；单独载入本文件时，须同时提供可访问的规范仓库。

可直接用自然语言说明请求。沿用参数写法时使用：

`[项目路径] [--plan] [--type auto|lib|app|assets|dataset|content|research|workspace]`

- 路径省略时使用当前目录，带空格的路径用引号。遇到多个目标、无效路径、未知参数或冲突类型时先报告问题。
- `--plan` 和“只读盘点”均使用流程中的只读模式，不修改任何文件。
- `--type` 采用[三层正交模型](../../docs/repository-types.md)的 6 类核心原型与多仓拓扑 `workspace`，默认 `auto`。兼容 v1 别名：`software` 按消费方式自动细分为 `lib` 或 `app`，`ros` 按包/系统形态细分为 `lib` 或 `app` 并启用 ROS 生态适配器。
- 用户明确要求整理或迁移时，在指定范围内实施并补齐最小防退化护栏。以规范仓库自身为目标时仅做只读盘点。

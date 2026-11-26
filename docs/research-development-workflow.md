# 项目在哪里开发、怎样测试、如何整理

调研于 2026-11-26。开发时从项目自身的 README、依赖清单和测试入口开始。整理时从方向索引找到项目，记录哪个仓库维护代码、哪台机器能运行、最近验证了什么。两处用链接关联。

## 上游项目

下表记录项目维护者写入仓库的开发步骤和交付方式。链接固定到所查提交。此次核对了文档和配置，未在本地运行上游项目。

| 项目与交付物 | 维护者改哪里 | 怎样验证或交付 | 一手来源 |
| --- | --- | --- | --- |
| LeRobot · 机器人采集与学习工具 | 实现在 `src/lerobot/`。采集、回放、训练由 `pyproject.toml` 分别注册为 `lerobot-record`、`lerobot-replay`、`lerobot-train`。 | 拉取 Git LFS 测试资源后，数据相关改动可用 `pytest -sv tests -m dataset` 检查。贡献指南说明了数据、硬件等测试各自需要的依赖。 | [命令注册](https://github.com/huggingface/lerobot/blob/b07adcc5e3ce42c26a248236dbb3571f84c28c43/pyproject.toml#L405-L419) · [测试约定](https://github.com/huggingface/lerobot/blob/b07adcc5e3ce42c26a248236dbb3571f84c28c43/CONTRIBUTING.md#L55-L86) |
| Vue 官方文档 · 阅读站点 | 作者编辑 `src/` 里的 Markdown，小改动可直接在 GitHub 提 PR。站点依赖单独维护的 `@vue/theme`。 | 本地用 `pnpm i` 安装依赖，再用 `pnpm run dev` 看页面。Netlify 执行 `pnpm run build`，发布 `.vitepress/dist`。 | [作者指南](https://github.com/vuejs/docs/blob/f66b5825d64a722ea6abc6eaae9974aa09c0c109/README.md#L3-L28) · [部署配置](https://github.com/vuejs/docs/blob/f66b5825d64a722ea6abc6eaae9974aa09c0c109/netlify.toml#L4-L6) |
| uv · 命令行软件 | 根 `Cargo.toml` 把 `crates/*` 纳入同一工作区。改动可以定位到相应 crate，开发版 CLI 可通过 `cargo run -- venv` 实际调用。 | 贡献者可以用 nextest 按名称选测试。维护者用脚本准备版本变更，发版本 PR，合并后启动发布工作流。 | [工作区配置](https://github.com/astral-sh/uv/blob/9bf01bef71c76643290ca17635970076fab1bd0d/Cargo.toml#L1-L11) · [测试入口](https://github.com/astral-sh/uv/blob/9bf01bef71c76643290ca17635970076fab1bd0d/CONTRIBUTING.md#L63-L71) · [开发版 CLI](https://github.com/astral-sh/uv/blob/9bf01bef71c76643290ca17635970076fab1bd0d/CONTRIBUTING.md#L140-L147) · [发布流程](https://github.com/astral-sh/uv/blob/9bf01bef71c76643290ca17635970076fab1bd0d/CONTRIBUTING.md#L366-L389) |
| Diffusion Policy · 论文实验与复现 | 复现者按任务和方法取回数据及配置。多随机种子的示例把每次训练写入各自的 `train_*`，再把汇总指标写入 `metrics/`。 | 论文提供配置、逐次训练日志、检查点，并说明论文数字对应的聚合字段。复核者可下载指定检查点交给 `eval.py`，在自己的输出目录检查评估结果。 | [已发布的实验证据](https://github.com/real-stanford/diffusion_policy/blob/5ba07ac6661db573af695b419a7947ecb704690f/README.md#L26-L61) · [仿真数据、训练与评估步骤](https://github.com/real-stanford/diffusion_policy/blob/5ba07ac6661db573af695b419a7947ecb704690f/README.md#L110-L237) |

## 对本规范的启发

- 采集与回放可以共享一个包，同时为现场操作者提供独立命令。开发说明可以直接指向验证本次改动的那组测试。
- 内容站点的 README 应告诉作者正文在哪、怎样预览。部署配置应能指出读者最终会看到哪份构建产物。
- 软件项目可以分别说明贡献者怎样运行改动、维护者怎样发布版本。研究项目还需要说明如何从报告中的数字找回对应的配置、运行记录和聚合方法。

## 个人项目多了以后怎么找

Simon Willison 的 Datasette 把环境和测试写进贡献指南。改动时用 `uv run pytest` 跑常规测试，涉及浏览器行为时还有单独的 Playwright 入口。他的个人研究合集采用另一种做法：每项研究各有目录和 README，首页按各 README 首次提交的时间生成项目索引。可以借鉴这种索引，将已有的独立仓库直接列为链接。[Datasette 贡献指南](https://docs.datasette.io/en/latest/contributing.html) · [研究合集的索引生成说明](https://github.com/simonw/research#updating-this-readme)

当组件必须一起运行时，可以维护一份组合清单。ROS 2 的 `ros2.repos` 逐项记录路径、Git 地址和版本，其中有些版本指向会前进的分支。你的实验要重现某次运行时，可以补记当时各组件实际使用的提交。[ROS 2 组件清单](https://github.com/ros2/ros2/blob/rolling/ros2.repos)

## 在自己的项目中怎么用

| 时机 | 去哪里、用什么 | 做到什么就够了 |
| --- | --- | --- |
| 改功能 | 在实际 Git 工作副本里看 README、依赖清单和已有测试。仓库用 uv、pnpm、Conda 或 ROS 工具链就沿用。新建且适合的 Python 项目可优先用 Pixi。 | 能指出使用者通过哪个命令、页面或文件用到这次改动。 |
| 验证改动 | 先跑受影响的快测。动捕和跟踪用短回放检查输入输出，训练用开发集和固定配置对比指标，内容站点预览一页并打开图片。 | 记录测试结果及范围。涉及硬件时，把现场验收列为单独一项；模型定型后再按实验协议做留出集终验。 |
| 归档或接手项目 | 在项目总目录的方向索引登记主仓、工作副本与交付物。需要追踪跨仓的待办时，GitHub Projects 可以用表格或看板汇总 Issue 和 PR。[GitHub Projects 文档](https://docs.github.com/en/issues/planning-and-tracking-with-projects) | 从一行索引即可找到代码、可运行的位置及最近一次验证。 |
| 决定是否合并 | 对一个真实仓库运行 OMP 技能 `/skill:standardize-repo <实际仓库路径> --plan`，看入口、调用方和发布边界。多台主机上的副本先核对远端地址、分支、提交和本地改动。 | 共用格式可以在原仓共享。独立发布的数据、软件或报告可分别登记。只整理索引时，更新链接就够了。 |

### 两条本机验证过的开发命令

以下分别从各项目的根目录执行。

| 项目 | 命令 | 此次验证的范围 |
| --- | --- | --- |
| `mocap-label` | `uv run --isolated --locked --extra test python -m pytest -q -p no:cacheprovider tests/test_annotations.py` | 11 项通过，涵盖标注、规则预览、撤销等。已有虚拟环境缺少 pytest，使用隔离环境和仓库声明的 `test` 依赖后通过。 |
| `macaron-artifacts` | `node --test scripts/replay/*.test.mjs` | 3 项通过，涵盖回放事件、时长校验和本地接口回放。根 `package.json` 将它注册为 `replay:test`。 |

这两条命令验证了标注逻辑和回放接口。真机采集、完整训练和浏览器界面属于另外的验收范围。复现第一条命令还需相同的 `uv.lock`，检查当天该文件在本地工作副本中尚未纳入 Git。

### 一行索引怎么写

按实际研究方向组织索引。一个项目选一个主要归属，其他方向引用同一条目。下面展示填写方式，路径和提交用示例值表示。

| 方向 | 项目 / 主仓地址 | 类型 | 工作副本 | 最近验证 |
| --- | --- | --- | --- | --- |
| motion-labeling | 动捕标注工具 / `<主仓 URL>` | A 软件 | 开发机 `~/work/mocap-label` | 2026-11-26，标注测试 11 项通过，本地 HEAD `<提交号>` |

同一项目在采集机或标注机有副本时，沿用同一条目，补记主机、路径和职责。跨机核对优先看 Git 提交和未提交改动；文件夹时间可用于筛选待盘点项目。若交付数据或实验报告，再链接到带版本的清单或报告。训练日志和大文件保留在实际存储位置。

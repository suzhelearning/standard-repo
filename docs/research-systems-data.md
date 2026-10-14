# 规划、导航、感知、原生库与数据发布：研究记录

访问日期：2026-10-14。范围：官方仓库目录、README 和 ROS 官方文档；未安装、构建或运行这些项目。以下路径是本次页面所见，默认分支会变化，不是固定版本审计。每节将观察与本设计建议分开。

## 1. MoveIt 2：运动规划的多包仓库

来源：[官方仓库](https://github.com/moveit/moveit2)。

观察：仓库包含 `moveit_core/`、`moveit_configs_utils/` 等多个包。`moveit_configs_utils/` 内有 `package.xml`、`setup.py`、同名 Python 包、`default_configs/` 和 `test/`；`moveit_core/` 有自己的 `CMakeLists.txt`。根目录还有 `.docker/` 和 `.repos` 文件。

建议：ROS 系统不能强制套一个 Python 包。包级构建、配置和测试应保持就近归属；多包不等于必须多 Git 仓库。

不照搬：MoveIt 的完整包数量、插件分类以及全部 CI 文件不适合小型遥操作项目。

## 2. Nav2：导航与启动资源

来源：[仓库](https://github.com/ros-navigation/navigation2/tree/main)、[nav2_bringup 目录](https://github.com/ros-navigation/navigation2/tree/main/nav2_bringup)、[该目录 API](https://api.github.com/repos/ros-navigation/navigation2/contents/nav2_bringup)。

观察：根目录按 `nav2_amcl/`、`nav2_controller/`、`nav2_planner/`、`nav2_msgs/`、`nav2_system_tests/` 等包组织。`nav2_bringup/` 包含 `launch/`、`params/`、`maps/`、`graphs/`、`rviz/`、`package.xml` 和 `CMakeLists.txt`。

建议：启动描述、导航地图、路线图和可视化配置是实际存在的文件种类，不应全塞进辅助 `scripts/`。系统级资源可属于 bringup 包，地图也不等于物理仿真的环境网格。

不照搬：不为一个只处理手部轨迹的项目创建导航、地图或行为树目录。

## 3. ros2_control：控制与硬件接口

来源：[官方仓库](https://github.com/ros-controls/ros2_control)。

观察：公开目录展示 `controller_interface/` 包，其内部有 `include/controller_interface/`、`include/semantic_components/`、`src/`、`test/`、`package.xml` 和 `CMakeLists.txt`。根目录 `.docker/` 组织构建／发布容器。

建议：驱动与控制方向需要支持 C++ 公共头文件和原生构建；Python 优先不应成为所有仓库必须带 `pyproject.toml` 的理由。

不照搬：不能把容器配置、控制包存在视为真机部署或安全性已经验证。

## 4. ROS 工作区不等于源码仓库

来源：[ROS 2 Jazzy 官方工作区教程](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)。

观察：教程把仓库检出在 `ros2_ws/src/`，构建后生成 `build/`、`install/`、`log/`。依赖通过包内 `package.xml` 声明，overlay 是构建后的环境。

建议：模板必须明确画的是“源码仓库内部”还是“本地工作区”。源码仓库不需要提交 `build/`、`install/`、`log/`，也不应该复制另一环境的 overlay。

## 5. Pinocchio：运动学／动力学原生算法库

来源：[官方目录 API](https://api.github.com/repos/stack-of-tasks/pinocchio/contents/)、[仓库 devel 分支](https://github.com/stack-of-tasks/pinocchio/tree/devel)。

观察：根目录有 `include/`、`src/`、`bindings/`、`examples/`、`benchmark/`、`unittest/`、`CMakeLists.txt`、`package.xml`、`pyproject.toml` 和 Pixi 文件。

建议：软件型模板应提供原生库变体：公共头文件、实现与语言绑定各有位置。性能基准程序与它生成的结果需要区分。

不照搬：文件共存不表示每个项目都需要多种构建工具；不能从该目录推断所有项目都该统一 Pixi。

## 6. FoundationPose：感知、重建与混合语言

来源：[NVlabs 官方仓库及 README](https://github.com/NVlabs/FoundationPose)。

观察：`learning/` 下按 `datasets/`、`models/`、`training/` 分类；还有 `bundlesdf/`、`mycpp/`、`docker/`，其中 `mycpp/` 有 CMake、头文件及实现。README 要求另行下载权重与演示数据，输出目录可通过参数指定。其 `assets/` 在本次目录中主要是论文展示图片和视频。

建议：感知代码可使用软件型模板的混合语言扩展，不必新增感知专属根目录标准。不能仅凭 `assets` 名称就断言里面是机器人资产；本标准建议将文档媒体放 `docs/media/`，物理资源放 `assets/`，这是我们选择的约定，不是上游事实。

不照搬：论文代码根目录散布多个入口和工具文件，不是希望复制的长期维护布局。

## 7. Open X-Embodiment：数据发布不等于数据处理代码

来源：[官方仓库及 README](https://github.com/google-deepmind/open_x_embodiment)。

观察：源码仓库主要包含 `colabs/`、`models/`、`imgs/`、README 等；数据以 RLDS episode 形式描述，README 链接数据目录表，并给出从云存储获取数据和 checkpoint 的方式。完整数据不以根目录下的 Git 轨迹文件集合展示。

建议：区分“执行清洗／渲染／导出的软件仓库”和“交付某个版本数据集的发布仓库”。前者使用软件型模板；后者可以只维护说明、格式定义、清单、分割与小样本，数据实体位于外部存储。这些建议目录不是 Open X-Embodiment 原样目录。

## 8. Isaac ROS Pose Estimation：同一算法方向的系统化交付

来源：[官方仓库及 README](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_pose_estimation)，也是 FoundationPose 官方 README 指向的 ROS 版本。

观察：根目录按 `isaac_ros_foundationpose/`、`isaac_ros_foundationpose_models_install/`、`isaac_ros_centerpose/` 等组织。README 将部署后的节点组合与推理依赖分开说明，并链接独立 benchmark 仓库的程序与结果。

建议：同属姿态估计方向，研究代码和 ROS 部署代码可以需要不同布局；“项目研究什么”不足以决定模板。模型获取可作为专门的安装职责，但不要求每个小项目都为此建独立包。上游发布了性能数字不代表本机复现过，本轮不评价实际性能。

## 收敛结论

这些一手来源支持按交付物和构建方式划分模板，而不是按研究关键词分仓：

- 软件包：算法、感知、离线处理；原生绑定是变体。
- ROS 多包系统：控制、规划、导航与系统启动，保留包级构建习惯。
- 数据发布：格式、清单、来源、使用说明与外部数据引用，不强制有源码包。

机器人／物体／环境资源与学习仿真方向见另外两份研究记录。以上是设计归纳，不是行业标准声明。

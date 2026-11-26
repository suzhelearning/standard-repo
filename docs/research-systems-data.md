# 规划、导航、感知、原生库与数据发布：研究记录

调研日期为 2026-10-14。以下记录来自当时的官方文档和源码，默认分支可能变化。本次仅核对文档与路径。目录选型见[仓库类型与布局](repository-types.md)。

## 1. MoveIt 2：运动规划的多包仓库

来源：[官方仓库](https://github.com/moveit/moveit2)。

观察：仓库包含 `moveit_core/`、`moveit_configs_utils/` 等多个包。`moveit_configs_utils/` 内有 `package.xml`、`setup.py`、同名 Python 包、`default_configs/` 和 `test/`；`moveit_core/` 有自己的 `CMakeLists.txt`。根目录还有 `.docker/` 和 `.repos` 文件。

## 2. Nav2：导航与启动资源

来源：[仓库](https://github.com/ros-navigation/navigation2/tree/main)、[nav2_bringup 目录](https://github.com/ros-navigation/navigation2/tree/main/nav2_bringup)、[该目录 API](https://api.github.com/repos/ros-navigation/navigation2/contents/nav2_bringup)。

观察：根目录按 `nav2_amcl/`、`nav2_controller/`、`nav2_planner/`、`nav2_msgs/`、`nav2_system_tests/` 等包组织。`nav2_bringup/` 包含 `launch/`、`params/`、`maps/`、`graphs/`、`rviz/`、`package.xml` 和 `CMakeLists.txt`。

## 3. ros2_control：控制与硬件接口

来源：[官方仓库](https://github.com/ros-controls/ros2_control)。

观察：公开目录展示 `controller_interface/` 包，其内部有 `include/controller_interface/`、`include/semantic_components/`、`src/`、`test/`、`package.xml` 和 `CMakeLists.txt`。根目录 `.docker/` 组织构建／发布容器。

## 4. ROS 工作区不等于源码仓库

来源：[ROS 2 Jazzy 官方工作区教程](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)。

观察：教程把仓库检出在 `ros2_ws/src/`，构建后生成 `build/`、`install/`、`log/`。依赖通过包内 `package.xml` 声明，overlay 是构建后的环境。

## 5. Pinocchio：运动学／动力学原生算法库

来源：[官方目录 API](https://api.github.com/repos/stack-of-tasks/pinocchio/contents/)、[仓库 devel 分支](https://github.com/stack-of-tasks/pinocchio/tree/devel)。

观察：根目录有 `include/`、`src/`、`bindings/`、`examples/`、`benchmark/`、`unittest/`、`CMakeLists.txt`、`package.xml`、`pyproject.toml` 和 Pixi 文件。

## 6. FoundationPose：感知、重建与混合语言

来源：[NVlabs 官方仓库及 README](https://github.com/NVlabs/FoundationPose)。

观察：`learning/` 下按 `datasets/`、`models/`、`training/` 分类；还有 `bundlesdf/`、`mycpp/`、`docker/`，其中 `mycpp/` 有 CMake、头文件及实现。README 要求另行下载权重与演示数据，输出目录可通过参数指定。其 `assets/` 在本次目录中主要是论文展示图片和视频。

## 7. Open X-Embodiment：数据发布不等于数据处理代码

来源：[官方仓库及 README](https://github.com/google-deepmind/open_x_embodiment)。

观察：源码仓库主要包含 `colabs/`、`models/`、`imgs/`、README 等；数据以 RLDS episode 形式描述，README 链接数据目录表，并给出从云存储获取数据和 checkpoint 的方式。完整数据不以根目录下的 Git 轨迹文件集合展示。

## 8. Isaac ROS Pose Estimation：同一算法方向的系统化交付

来源：[官方仓库及 README](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_pose_estimation)，也是 FoundationPose 官方 README 指向的 ROS 版本。

观察：根目录按 `isaac_ros_foundationpose/`、`isaac_ros_foundationpose_models_install/`、`isaac_ros_centerpose/` 等组织。README 将部署后的节点组合与推理依赖分开说明，并链接独立 benchmark 仓库的程序与结果。

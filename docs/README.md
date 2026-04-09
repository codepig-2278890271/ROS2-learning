# ROS2 Python 学习示例

这是一个简单的 ROS2 Python 包示例，演示了基本的发布/订阅节点和 `turtlesim` 控制节点。

## 项目概述

- 包名：`python`
- 类型：ROS2 Python 包（`ament_python`）
- 主要功能：
  - `publisher_node.py`：向 `/chatter` 话题发布 `std_msgs/String` 消息
  - `subscriber_node.py`：订阅 `/chatter` 话题并打印接收到的字符串
  - `turtle_control.py`：向 `/turtle1/cmd_vel` 发布 `geometry_msgs/Twist`，让 `turtlesim` 小海龟运动
  - `launch/multi_nodes_launch.py`：同时启动发布者、订阅者、小海龟控制节点与 `turtlesim` 节点

## 目录结构

```text
src/python/
  package.xml
  setup.py
  setup.cfg
  launch/multi_nodes_launch.py
  python/
    publisher_node.py
    subscriber_node.py
    turtle_control.py
```

## 依赖

- ROS2
- `rclpy`
- `std_msgs`
- `geometry_msgs`
- `turtlesim`

## 编译与安装

在工作区根目录下执行：

```bash
colcon build --packages-select python
```

构建完成后，执行：

```bash
source install/setup.bash
```

## 运行示例

### 1. 单独启动发布者节点

```bash
ros2 run python pub
```

### 2. 单独启动订阅者节点

```bash
ros2 run python sub
```

### 3. 单独启动 `turtle` 控制节点

```bash
ros2 run python turtle
```

### 4. 使用 Launch 一次启动所有节点

```bash
ros2 launch python multi_nodes_launch.py
```

这个 launch 文件会同时启动：
- `py_publisher_node`
- `py_subscriber_node`
- `turtle_control_node`
- `turtlesim_node`

## 节点简介

### `publisher_node.py`

- 节点名：`py_publisher_node`
- 发布话题：`chatter`
- 消息类型：`std_msgs/String`
- 每秒发布一条字符串消息

### `subscriber_node.py`

- 节点名：`py_subscriber_node`
- 订阅话题：`chatter`
- 每次收到消息时打印日志

### `turtle_control.py`

- 节点名：`turtle_control_node`
- 发布话题：`/turtle1/cmd_vel`
- 消息类型：`geometry_msgs/Twist`
- 0.5 秒发布一次速度命令，让 `turtlesim` 小海龟前进并转弯

## 备注

- 如果使用 `turtlesim`，请确保已安装并可正常运行 `turtlesim` 包。
- 本项目适合 ROS2 入门学习，演示节点创建、发布/订阅、定时器以及 launch 启动机制。

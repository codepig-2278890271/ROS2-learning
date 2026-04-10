# ROS2 Python 学习示例

这是一个简单的 ROS2 Python 包示例，演示了基本的发布/订阅节点、参数配置、服务通信和 `turtlesim` 控制节点。

## 项目概述

- 包名：`python`
- 类型：ROS2 Python 包（`ament_python`）
- 主要功能：
  - `publisher_node.py`：向 `/chatter` 话题发布 `std_msgs/String` 消息（支持参数配置）
  - `subscriber_node.py`：订阅 `/chatter` 话题并打印接收到的字符串
  - `turtle_control.py`：向 `/turtle1/cmd_vel` 发布 `geometry_msgs/Twist`，让 `turtlesim` 小海龟运动（支持参数配置）
  - `service_node.py`：提供 LED 控制服务（`/toggle_led`）
  - `service_client.py`：调用 LED 控制服务的客户端
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
    service_node.py
    service_client.py
```

## 依赖

- ROS2
- `rclpy`
- `std_msgs`
- `geometry_msgs`
- `std_srvs`
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

### 1. 发布/订阅示例

#### 单独启动发布者节点

```bash
ros2 run python pub
```

#### 使用参数配置发布者

```bash
ros2 run python pub --ros-args -p publish_rate:=2.0 -p message_prefix:="快速消息："
```

#### 单独启动订阅者节点

```bash
ros2 run python sub
```

### 2. TurtleSim 控制示例

#### 单独启动 `turtle` 控制节点

```bash
ros2 run python turtle
```

#### 使用参数配置 turtle 控制

```bash
ros2 run python turtle --ros-args -p linear_speed:=2.0 -p angular_speed:=1.0 -p control_rate:=0.2
```

### 3. 服务通信示例

#### 启动服务节点

```bash
ros2 run python service
```

#### 调用服务切换 LED 状态

```bash
ros2 run python client true
```

#### 调用服务查询 LED 状态

```bash
ros2 run python client false
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
- 支持参数：
  - `publish_rate` (float, 默认1.0)：发布频率（秒）
  - `message_prefix` (str, 默认"Python 发消息：")：消息前缀

### `subscriber_node.py`

- 节点名：`py_subscriber_node`
- 订阅话题：`chatter`
- 每次收到消息时打印日志

### `turtle_control.py`

- 节点名：`turtle_control_node`
- 发布话题：`/turtle1/cmd_vel`
- 消息类型：`geometry_msgs/Twist`
- 支持参数：
  - `linear_speed` (float, 默认1.0)：线速度
  - `angular_speed` (float, 默认0.5)：角速度
  - `control_rate` (float, 默认0.5)：控制频率（秒）

### `service_node.py`

- 节点名：`service_node`
- 服务名：`/toggle_led`
- 服务类型：`std_srvs/SetBool`
- 功能：模拟LED开关控制
- 请求参数：`bool data` (true=切换状态，false=查询状态)
- 响应：`bool success + string message`

### `service_client.py`

- 节点名：`service_client_node`
- 调用服务：`/toggle_led`
- 功能：LED控制服务的客户端
- 命令行参数：`true` (切换) 或 `false` (查询)

## ROS2 概念演示

本项目演示了以下 ROS2 核心概念：

### 1. 话题通信（Topics）
- **异步通信**：发布者发布消息，订阅者接收消息
- 示例：`publisher_node.py` ↔ `subscriber_node.py`

### 2. 服务通信（Services）
- **同步通信**：客户端请求，服务端响应
- 示例：`service_client.py` ↔ `service_node.py`

### 3. 参数系统（Parameters）
- 运行时配置节点行为
- 示例：发布频率、消息前缀、速度控制等

### 4. Launch 文件
- 同时启动多个节点
- 示例：`multi_nodes_launch.py`

## 调试命令

```bash
# 查看话题列表
ros2 topic list

# 查看服务列表
ros2 service list

# 查看节点参数
ros2 param list /node_name

# 手动发布消息
ros2 topic pub --once /chatter std_msgs/msg/String "data: 'test'"

# 手动调用服务
ros2 service call /toggle_led std_srvs/srv/SetBool "data: true"
```

## 备注

- 如果使用 `turtlesim`，请确保已安装并可正常运行 `turtlesim` 包。
- 本项目适合 ROS2 入门学习，演示节点创建、发布/订阅、服务通信、参数配置以及 launch 启动机制。
- 代码包含详细注释，适合学习 ROS2 Python API 使用方法。

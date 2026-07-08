# ros2_ws

ROS2 工作空间，基于 Humble + Python。

## 结构

```
ros2_ws/
├── src/                  # 源码（所有功能包放这里）
│   └── learning_node/    # 学习用的 Python 功能包
├── build/                # 编译中间文件（不入 git）
├── install/              # 编译产物（不入 git）
└── log/                  # 编译日志（不入 git）
```

## 编译

```bash
cd ~/ROS2-Learning/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## 功能包

| 包名 | 类型 | 说明 |
|------|------|------|
| learning_node | ament_python | 练习用包，学习节点、话题、服务等基础概念 |

## 运行

```bash
ros2 run learning_node timer_printer
```

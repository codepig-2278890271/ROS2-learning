# Launch 文件

## 为什么需要 Launch 文件

学到现在，你每次跑 demo 都要开好几个终端：

```bash
# 终端1：服务端
ros2 run learning_service add_two_ints_server

# 终端2：客户端
ros2 run learning_service add_two_ints_client

# 终端3：再跑个话题发布者
ros2 run learning_topic number_publisher
```

三个节点还好。想象一个真实机器人系统：相机驱动、激光雷达、定位、路径规划、电机控制……几十个节点，手动开？不现实。

**Launch 文件就是「一键启动多个节点」的脚本。**

```
ros2 launch <包名> <launch文件>

# 一个命令，起所有节点，带参数，带配置——全自动
```

---

## Launch 文件三种写法

ROS2 支持三种格式：

| 格式 | 后缀 | 推荐度 | 说明 |
|------|------|--------|------|
| **Python** | `_launch.py` | ⭐⭐⭐ | 最灵活，主流选择 |
| XML | `_launch.xml` | ⭐⭐ | 简单，适合静态配置 |
| YAML | `_launch.yaml` | ⭐ | 很少用 |

重点学 Python 版——写起来像脚本，可以用循环、条件、函数，灵活性完爆 XML。

---

## 第一个 Launch 文件：同时启动发布者和订阅者

在你已有的 `learning_topic` 包里新建 `launch/topic_demo_launch.py`：

```python
"""一键启动话题发布者 + 订阅者"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """返回「要启动哪些节点」的描述。这个函数是 launch 系统的入口。"""

    # ━━━ 节点1：发布者 ━━━
    publisher = Node(
        package='learning_topic',           # 功能包名
        executable='number_publisher',      # 可执行文件名（setup.py 里的 console_scripts 名）
        name='my_publisher',                # 节点名（运行时的名字，可以覆盖原来的）
    )

    # ━━━ 节点2：订阅者 ━━━
    subscriber = Node(
        package='learning_topic',
        executable='number_subscriber',
        name='my_subscriber',
    )

    # ━━━ 打包返回 ━━━
    return LaunchDescription([
        publisher,
        subscriber,
    ])
```

### 运行

```bash
colcon build
ros2 launch learning_topic topic_demo_launch.py
```

一个命令，两个节点同时启动。Ctrl+C 全部停掉。

---

## Launch 文件的核心：LaunchDescription

```
generate_launch_description()
        │
        ▼
   LaunchDescription([     ← 列表
       Node(...),          ← 要启的节点
       Node(...),          ← 要启的节点
       Node(...),          ← 要启的节点
       ...                 ← 还可以有参数、配置等
   ])
```

`LaunchDescription` 就是一个「启动清单」。除了 `Node`，还能往里放：

| 动作 | 作用 |
|------|------|
| `Node` | 启动一个节点 |
| `DeclareLaunchArgument` | 声明命令行参数 |
| `SetParameter` | 启动时设置参数 |
| `IncludeLaunchDescription` | 嵌套另一个 launch 文件 |
| `TimerAction` | 延迟启动 |
| `LogInfo` | 打印日志 |

---

## 启动时设置参数

节点里声明的参数，launch 文件可以直接传值：

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='learning_parameter',
            executable='param_demo',
            name='camera_node',
            parameters=[                          # ← 启动时设参数
                {'camera_width': 1280},
                {'camera_height': 720},
                {'frame_rate': 60},
                {'topic_name': '/camera/image'},
            ],
        ),
    ])
```

```bash
ros2 launch learning_parameter param_launch.py
# 节点一起动，参数已经设好了——不用再 ros2 param set
```

---

## 命令行参数：让 Launch 文件可配置

想同一个 launch 文件换不同机器人用？加命令行参数：

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # ━━━ ① 声明命令行参数 ━━━
    speed_arg = DeclareLaunchArgument(
        'speed',                          # 参数名
        default_value='1.0',              # 默认值
        description='发布频率 (Hz)',       # 描述
    )

    text_arg = DeclareLaunchArgument(
        'text',
        default_value='hello',
        description='发布的消息内容',
    )

    # ━━━ ② 用 LaunchConfiguration 取参数值 ━━━
    speed = LaunchConfiguration('speed')
    text = LaunchConfiguration('text')

    return LaunchDescription([
        speed_arg,
        text_arg,
        Node(
            package='learning_parameter',
            executable='param_demo',
            name='demo_node',
            parameters=[{
                'frame_rate': speed,       # ← 用命令行参数
                'topic_name': text,
            }],
        ),
    ])
```

```bash
# 用默认值启动
ros2 launch my_pkg demo_launch.py

# 覆盖参数
ros2 launch my_pkg demo_launch.py speed:=5.0 text:="custom_topic"
```

`:=` 是 launch 系统专用的**参数赋值语法**，和 `ros2 param set` 的赋值不一样。

---

## 话题重映射：改节点的话题名

不改源码，让节点用不同的话题名通信：

```python
Node(
    package='learning_topic',
    executable='number_publisher',
    name='pub1',
    remappings=[
        ('number_topic', 'renamed_topic'),  # 原话题名 → 新话题名
    ],
)
```

**超实用场景**：同一个发布者代码启动两个实例，映射到不同话题：

```python
return LaunchDescription([
    # 实例1：发布到 /camera_left
    Node(
        package='learning_topic',
        executable='number_publisher',
        name='left_camera',
        remappings=[('number_topic', 'camera_left')],
        parameters=[{'frame_rate': 30}],
    ),
    # 实例2：同一个代码，发布到 /camera_right
    Node(
        package='learning_topic',
        executable='number_publisher',
        name='right_camera',
        remappings=[('number_topic', 'camera_right')],
        parameters=[{'frame_rate': 30}],
    ),
])
```

代码只写一份，launch 文件让它「分身」跑成多个实例。

---

## 完整的 Launch 文件示例：起一个机器人系统

把 `learning_topic` 的发布者/订阅者加上 `learning_parameter` 的参数节点，一起启动：

```python
"""启动完整的话题演示系统

用法：
  ros2 launch learning_topic system_launch.py
  ros2 launch learning_topic system_launch.py rate:=10.0
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # 命令行参数
    rate_arg = DeclareLaunchArgument('rate', default_value='2.0',
                                     description='发布频率 (Hz)')
    rate = LaunchConfiguration('rate')

    # 发布者
    pub_node = Node(
        package='learning_topic',
        executable='number_publisher',
        name='number_publisher',
        parameters=[{'publish_rate': rate}],
    )

    # 订阅者
    sub_node = Node(
        package='learning_topic',
        executable='number_subscriber',
        name='number_subscriber',
    )

    return LaunchDescription([
        rate_arg,
        LogInfo(msg=['🚀 启动系统，发布频率: ', rate, ' Hz']),
        pub_node,
        sub_node,
    ])
```

---

## 包结构：launch 文件放哪

```
learning_topic/
├── launch/                        # ← 新建这个目录
│   ├── topic_demo_launch.py
│   └── system_launch.py
├── learning_topic/
│   ├── __init__.py
│   ├── number_publisher.py
│   └── number_subscriber.py
├── setup.py
├── package.xml
└── ...
```

别忘了在 `setup.py` 里注册 launch 目录：

```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'learning_topic'

setup(
    # ... 其他配置不变 ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ━━━ 注册 launch 文件 ━━━
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*_launch.py')),
    ],
    # ...
)
```

> glob 用相对路径即可（colcon 构建时工作目录就是包源码目录）。模式是 `*_launch.py`（下划线），不是 `*.launch.py`（点号）。

> 每新建一个带 launch 文件的包，都要加这段。不然 `ros2 launch` 找不到。

---

## 嵌套 Launch：一个 launch 调另一个

你会在 `learning_topic/launch/` 里写一个 `topic_demo_launch.py`，在 `learning_service/launch/` 里写一个 `service_demo_launch.py`。然后写一个顶层 launch 把它们全包进来：

```python
"""全部启动 —— 话题 + 服务 + 参数"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 找到子 launch 文件的路径
    topic_launch = PythonLaunchDescriptionSource([
        FindPackageShare('learning_topic'), '/launch/topic_demo_launch.py'
    ])
    service_launch = PythonLaunchDescriptionSource([
        FindPackageShare('learning_service'), '/launch/service_demo_launch.py'
    ])

    return LaunchDescription([
        IncludeLaunchDescription(topic_launch),
        IncludeLaunchDescription(service_launch),
    ])
```

---

## Launch 文件 vs 手动开终端

| | 手动 ros2 run | Launch 文件 |
|------|-------------|-------------|
| 启动 N 个节点 | 开 N 个终端 | 一个命令 |
| 设参数 | 每次 ros2 param set | 写在文件里，启动即生效 |
| 话题重映射 | 命令行加 --ros-args | 写在文件里 |
| 可复现 | 靠记忆力 | 靠文件 |
| CI / 自动化 | 没法搞 | 天生支持 |
| 团队协作 | 「你去问老王怎么启」 | 看 launch 文件一目了然 |

---

## 常用模式速查

```python
# 启动节点
Node(package='包名', executable='可执行文件名', name='运行时节点名')

# 设参数
Node(..., parameters=[{'键': 值}, ...])

# 话题重映射
Node(..., remappings=[('原话题', '新话题')])

# 命令行参数
DeclareLaunchArgument('参数名', default_value='默认值')
LaunchConfiguration('参数名')   # 取值

# 嵌套 launch
IncludeLaunchDescription(PythonLaunchDescriptionSource([路径]))

# 找包路径
from launch_ros.substitutions import FindPackageShare
FindPackageShare('包名')  # 返回包的 share 目录路径
```

---

## 总结

```
Launch 文件 = 一键启动多个节点的脚本

核心概念：
  LaunchDescription         启动清单
  Node                      要启动的节点
  parameters                启动时设参数
  remappings                话题重映射
  DeclareLaunchArgument     命令行参数 := 赋值
  IncludeLaunchDescription  嵌套启动

文件位置：
  包的 launch/*.launch.py  →  setup.py 里注册 →  ros2 launch 找到

一句话：
  以后跑任何 demo，第一个写的不应该是 ros2 run，而是 launch 文件。
```

学会了 Launch，**参数 + Launch = 可配置的一键启动系统**。同一个代码，不同 launch 文件配不同参数和重映射，就能跑出不同的行为——这才像个正经机器人项目了。

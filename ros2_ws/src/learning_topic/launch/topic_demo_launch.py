"""Launch 文件模版：一键启动多个 ROS2 节点

┌─────────────────────────────────────────────────────────────┐
│ 以后你给新项目写 launch 文件，复制这个文件改三处：           │
│                                                             │
│ ① Node(package='你的包名', ...)   ← setup.py 里的包名        │
│ ② executable='可执行文件名'       ← setup.py entry_points 名 │
│ ③ name='运行时节点名'             ← ros2 node list 看到的名  │
│                                                             │
│ 文件还必须放在 包/launch/ 目录下，命名为 xxx_launch.py。      │
│ setup.py 里要用 glob('launch/*_launch.py') 注册。            │
└─────────────────────────────────────────────────────────────┘

用法：
  ros2 launch learning_topic topic_demo_launch.py
"""

from launch import LaunchDescription      # 启动清单：把要启动的东西打包
from launch_ros.actions import Node        # Node：代表一个 ROS2 节点


def generate_launch_description():
    """返回 LaunchDescription，告诉 launch 系统要启动哪些节点"""

    return LaunchDescription([

        # ── 节点1：发布者 ──
        Node(
            package='learning_topic',       # 功能包名（package.xml 里的 <name>）
            executable='number_publisher',  # 可执行文件名（setup.py 的 entry_points 里注册的）
            name='number_publisher',        # 运行时节点名（ros2 node list 看到的名字）
            # 可选参数（需要时取消注释）：
            # parameters=[{'参数名': 值}],  # 启动时设置参数值
            # remappings=[('旧话题', '新话题')],  # 话题重映射
        ),

        # ── 节点2：订阅者 ── 加一个节点就加一个 Node(...),
        Node(
            package='learning_topic',
            executable='number_subscriber',
            name='number_subscriber',
        ),

    ])

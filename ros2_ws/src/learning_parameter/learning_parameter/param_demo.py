"""参数基础演示 —— 声明、读取、CLI 修改

运行方式：
  ros2 run learning_parameter param_demo
  # 然后在另一个终端里试：
  ros2 param list
  ros2 param get /param_demo camera_width
  ros2 param set /param_demo camera_width 1280
"""

import rclpy
from rclpy.node import Node


class ParamDemo(Node):
    """声明参数 → 读取参数 → 用参数控制节点行为"""

    def __init__(self):
        super().__init__('param_demo')

        # ━━━ ① 声明参数（键 = 默认值）━━━
        self.declare_parameter('camera_width', 640)        # int
        self.declare_parameter('camera_height', 480)       # int
        self.declare_parameter('frame_rate', 30.0)         # double
        self.declare_parameter('topic_name', '/image_raw') # string
        self.declare_parameter('enable_debug', False)      # bool

        self.get_logger().info('参数已声明，试试 ros2 param list / get / set')

        # ━━━ ② 创建定时器，每秒打印一次当前参数 ━━━
        self._timer = self.create_timer(2.0, self.print_params)

    def print_params(self):
        """定时打印所有参数值 —— 用 ros2 param set 改值后可以看到变化"""
        # 读参数：.value 自动推断类型
        w = self.get_parameter('camera_width').value
        h = self.get_parameter('camera_height').value
        rate = self.get_parameter('frame_rate').value
        topic = self.get_parameter('topic_name').value
        debug = self.get_parameter('enable_debug').value

        self.get_logger().info(
            f'当前参数: width={w}, height={h}, rate={rate}Hz, '
            f'topic="{topic}", debug={debug}'
        )


def main():
    rclpy.init()
    rclpy.spin(ParamDemo())


if __name__ == '__main__':
    main()

"""加法客户端（异步调用）

向 add_two_ints 服务发送请求，等待并打印结果。

运行方式：
  ros2 run learning_service add_two_ints_client         # 默认 3 + 5
  ros2 run learning_service add_two_ints_client 10 20   # 10 + 20
"""

import sys
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class AddTwoIntsClient(Node):
    """加法客户端节点"""

    def __init__(self):
        super().__init__('add_two_ints_client')

        # ① 创建客户端
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # ② 等待服务端上线
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('⏳ 等待服务端上线…')
        self.get_logger().info('✅ 服务端已连接')

    def send_request(self, a, b):
        """发送异步请求"""
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        self.get_logger().info(f'发送: {a} + {b}')
        return self.cli.call_async(request)


def main():
    rclpy.init()
    node = AddTwoIntsClient()

    # ━━━ 命令行参数 ━━━
    # sys.argv 是 Python 自带的命令行参数列表
    #   ros2 run learning_service add_two_ints_client 10 20
    #                        ↑ argv[0]            argv[1] argv[2]
    # ros2 会自动把 --ros-args 那堆内部参数过滤掉，
    # 所以 sys.argv 里只剩下 python3 add_two_ints_client 10 20
    if len(sys.argv) >= 3:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    else:
        a, b = 3, 5  # 没传参数就用默认值

    future = node.send_request(a, b)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        node.get_logger().info(f'结果: {a} + {b} = {response.sum}')
    except Exception as e:
        node.get_logger().error(f'服务调用失败: {e}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

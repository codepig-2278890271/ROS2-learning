"""加法服务端

提供 add_two_ints 服务：接收两个整数 a 和 b，返回它们的和 sum。

运行方式：
  ros2 run learning_service add_two_ints_server
"""

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class AddTwoIntsServer(Node):
    """提供加法服务的节点"""

    def __init__(self):
        super().__init__('add_two_ints_server')

        # 创建服务端：服务类型、服务名、回调函数
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add_two_ints_callback
        )
        self.get_logger().info('🔧 服务端已启动，等待请求…')

    def add_two_ints_callback(self, request, response):
        """收到请求时自动调用，计算 a + b 并返回"""
        response.sum = request.a + request.b
        self.get_logger().info(f'收到: {request.a} + {request.b} = {response.sum}')
        return response


def main():
    rclpy.init()
    node = AddTwoIntsServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

"""动作客户端（Action Client）—— 找服务端 → 发目标 → 收反馈 → 拿结果

运行方式：
  ros2 run learning_action fibonacci_action_client         # 默认 order=5
  ros2 run learning_action fibonacci_action_client 10      # order=10
"""

import sys
from example_interfaces.action import Fibonacci
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._client = ActionClient(self, Fibonacci, 'fibonacci')
        self.get_logger().info('等待服务端…')
        self._client.wait_for_server()
        self.get_logger().info('服务端已连接')

    def send_goal(self, order):
        goal = Fibonacci.Goal()
        goal.order = order

        # ① 发送目标，注册反馈回调
        future = self._client.send_goal_async(goal, feedback_callback=self.on_feedback)

        # ② 服务端回复「接没接」后，绑 on_goal_response
        future.add_done_callback(self.on_goal_response)

        self.get_logger().info(f'目标已发送: order={order}')

    def on_goal_response(self, future):
        """服务端回复了：接受还是拒绝"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('目标被拒绝')
            return

        self.get_logger().info('目标被接受，等待结果…')

        # ③ 向服务端要最终结果，绑 on_result
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_result)

    def on_feedback(self, msg):
        """每次收到进度时触发（可能多次）"""
        self.get_logger().info(f'进度: {msg.feedback.sequence}')

    def on_result(self, future):
        """收到最终结果时触发（只触发一次）"""
        self.get_logger().info(f'结果: {future.result().result.sequence}')
        rclpy.shutdown()


def main():
    rclpy.init()

    # 创建客户端，发目标，然后 spin 等着收反馈和结果
    node = FibonacciActionClient()
    order = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    node.send_goal(order)
    rclpy.spin(node)


if __name__ == '__main__':
    main()

"""动作服务端（Action Server）—— 等目标 → 干活 → 发反馈 → 交结果

运行方式：
  ros2 run learning_action fibonacci_action_server
"""

import time
from example_interfaces.action import Fibonacci
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
        )
        self.get_logger().info('服务端启动，等待目标…')

    def goal_callback(self, goal_request):
        self.get_logger().info(f'收到目标: order={goal_request.order}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        _ = goal_handle  # 框架要求此参数，本例未使用
        self.get_logger().info('同意取消')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """在独立线程里跑，慢慢干活，边干边报进度"""
        sequence = [0, 1]
        feedback = Fibonacci.Feedback()

        for i in range(1, goal_handle.request.order):
            # 算下一项
            sequence.append(sequence[i] + sequence[i - 1])
            # 发反馈
            feedback.sequence = sequence
            goal_handle.publish_feedback(feedback)
            # 模拟耗时
            time.sleep(1.0)
            # 被取消就停
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('已取消')
                return Fibonacci.Result()

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence
        self.get_logger().info('计算完成')
        return result


def main():
    rclpy.init()
    rclpy.spin(FibonacciActionServer())


if __name__ == '__main__':
    main()

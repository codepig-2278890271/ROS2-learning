import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class NumberSubscriber(Node):
    def __init__(self):
        super().__init__('number_subscriber')
        # 创建订阅者：话题名 /number，消息类型 Int32，队列深度 10，回调函数
        self.subscription = self.create_subscription(
            Int32,                                 # 消息类型，必须和发布者一致
            'number',                              # 话题名，必须和发布者一致
            self.listener_callback,                # 收到消息时调用的函数
            10                                     # QoS 队列深度
        )

    def listener_callback(self, msg):
        squared = msg.data ** 2                    # 收到数字后做点处理：求平方
        self.get_logger().info(
            f'收到：{msg.data} → 平方后：{squared}'
        )


def main():
    rclpy.init()
    node = NumberSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

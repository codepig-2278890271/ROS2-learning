import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__("py_subscriber_node")

        # 创建订阅者，监听话题 chatter
        self.subscription = self.create_subscription(
            String,
            "chatter",
            self.listener_callback,
            10
        )

    # 收到消息就自动跑这个函数
    def listener_callback(self, msg):
        self.get_logger().info(f"收到：{msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
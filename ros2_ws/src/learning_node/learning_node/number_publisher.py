import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32                   # 导入 Int32 消息类型


class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher')       # 节点名
        self.count = 0                             # 计数器，每发一次 +1
        # 创建发布者：话题名 /number，消息类型 Int32，队列深度 10
        self.publisher = self.create_publisher(
            Int32,                                 # 消息类型
            'number',                              # 话题名（推荐用小写字母+下划线）
            10                                     # QoS 队列深度（暂存多少条待发消息）
        )
        # 定时器：每 2 秒调一次回调，发布一条消息
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = Int32()                              # 创建一条 Int32 消息
        msg.data = self.count                      # 把计数器的值塞进消息的 data 字段
        self.publisher.publish(msg)                # 发布！
        self.get_logger().info(f'发布：{msg.data}') # 日志输出
        self.count += 1                            # 计数器 +1


def main():
    rclpy.init()
    node = NumberPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

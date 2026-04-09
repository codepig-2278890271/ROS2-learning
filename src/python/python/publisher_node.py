# 导入 ROS2 Python 核心库
import rclpy
# 导入节点类
from rclpy.node import Node
# 导入字符串消息类型
from std_msgs.msg import String

# 定义一个节点类，继承自 Node
class PublisherNode(Node):

    # 构造函数：节点启动时先跑这里
    def __init__(self):
        # 给节点起名字：py_publisher_node
        super().__init__("py_publisher_node")

        # 创建发布者
        # 消息类型：String
        # 话题名：chatter
        # 队列长度 10
        self.publisher_ = self.create_publisher(String, "chatter", 10)

        # 创建定时器，每 1 秒跑一次回调函数
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    # 定时器到点就跑这个函数
    def timer_callback(self):
        # 新建一条消息
        msg = String()
        msg.data = f"Python 发消息：{self.count}"

        # 发布消息
        self.publisher_.publish(msg)

        # 打印日志
        self.get_logger().info(f"发布：{msg.data}")
        self.count += 1

# 主函数
def main(args=None):
    # 初始化 ROS2
    rclpy.init(args=args)

    # 创建节点
    node = PublisherNode()

    # 让节点一直跑
    rclpy.spin(node)

    # 关闭
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
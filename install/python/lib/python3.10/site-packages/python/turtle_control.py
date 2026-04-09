import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # 控制速度的消息类型

class TurtleControl(Node):
    def __init__(self):
        # 节点名字：turtle_control_node
        super().__init__("turtle_control_node")

        # 创建发布者
        # 话题名：/turtle1/cmd_vel（小海龟固定监听这个话题）
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        # 每隔0.5秒发一次指令
        self.timer = self.create_timer(0.5, self.timer_cb)

    def timer_cb(self):
        # 新建速度消息
        msg = Twist()

        # 线速度 x：向前走
        msg.linear.x = 1.0

        # 角速度 z：转弯
        msg.angular.z = 0.5

        # 发布消息
        self.pub.publish(msg)
        self.get_logger().info("小海龟正在跑圈～")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy                                            # ROS2 Python接口库
from rclpy.node import Node                             # ROS2节点类
import time

def main(args=None):                                    # ROS2节点入口main函数
    rclpy.init(args=args)                               # ROS2 Python接口初始化
    node = Node("hello_world_node")                     # 创建一个ROS2节点，名字叫hello_world_node

    while rclpy.ok():                                   # ROS2系统是否正常运行，循环直到ROS2系统关闭
        node.get_logger().info("Hello, World!")         # 打印日志，输出Hello, World!
        time.sleep(1)                                   # 休眠控制循环时间

    node.destroy_node()                                 # 销毁节点，清理资源
    rclpy.shutdown()                                    # 关闭ROS2系统
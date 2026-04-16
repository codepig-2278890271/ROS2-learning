import rclpy  # 导入ROS2的Python核心库
from rclpy.node import Node  # 导入节点模板类

# 定义自己的节点类，继承ROS2节点
class TestNode(Node):
    def __init__(self):  # 节点初始化函数，创建节点时自动运行
        super().__init__("test_py_node")  # 给节点起名字：test_py_node
        self.get_logger().info("Python 节点启动成功！")  # 打印一条日志

# 主函数，程序入口
def main():
    rclpy.init()  # 启动ROS2系统
    node = TestNode()  # 创建刚才写的节点
    rclpy.spin(node)  # 让节点一直运行，不退出
    node.destroy_node()  # 销毁节点（关闭时用）
    rclpy.shutdown()  # 关闭ROS2系统

# Python固定写法：运行这个文件时才执行main
if __name__ == '__main__':
    main()
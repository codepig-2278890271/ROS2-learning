import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node("fishros_python_node")
    node.get_logger().info("你好 FishROS Python Node!")
    rclpy.spin(node)
    # node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
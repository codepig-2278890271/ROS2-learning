import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
import sys

class ServiceClientNode(Node):
    def __init__(self):
        super().__init__('service_client_node')

        # 创建客户端
        self.cli = self.create_client(SetBool, 'toggle_led')

        # 等待服务可用
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待LED服务可用...')

        self.get_logger().info('LED服务已连接')

    def send_request(self, toggle_command):
        # 创建请求
        request = SetBool.Request()
        request.data = toggle_command  # True=切换状态，False=查询状态

        # 发送请求（异步）
        self.future = self.cli.call_async(request)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'服务响应: {response.message}')
        except Exception as e:
            self.get_logger().error(f'服务调用失败: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ServiceClientNode()

    # 从命令行参数获取操作
    # 运行方式: ros2 run python client true  (切换LED)
    # 运行方式: ros2 run python client false (查询LED状态)
    toggle_command = True  # 默认切换
    if len(sys.argv) > 1:
        toggle_command = sys.argv[1].lower() == 'true'

    node.send_request(toggle_command)

    # 等待响应
    rclpy.spin_until_future_complete(node, node.future)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
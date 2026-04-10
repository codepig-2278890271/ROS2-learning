import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool  # 使用标准的服务类型

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')

        # 创建服务
        # 服务名：toggle_led
        # 服务类型：SetBool (请求bool，返回bool+string)
        self.srv = self.create_service(
            SetBool,
            'toggle_led',
            self.toggle_led_callback
        )

        # 状态变量
        self.led_state = False
        self.get_logger().info('LED服务已启动，等待请求...')

    def toggle_led_callback(self, request, response):
        # request.data 是客户端发送的bool值
        if request.data:
            # 切换LED状态
            self.led_state = not self.led_state
            response.success = True
            response.message = f"LED已{'开启' if self.led_state else '关闭'}"
        else:
            # 只是查询状态
            response.success = True
            response.message = f"LED当前状态：{'开启' if self.led_state else '关闭'}"

        self.get_logger().info(f"收到请求: {request.data}, 响应: {response.message}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ServiceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
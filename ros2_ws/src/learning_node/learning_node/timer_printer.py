import rclpy                               # ROS2 的 Python 客户端库，一切功能的总入口
from rclpy.node import Node                # 导入 Node 类，所有节点都继承它


class TimerPrinter(Node):                  # 继承 Node，这是 ROS2 Python 的标准写法
    def __init__(self):                    # 构造函数：节点初始化时执行一次
        super().__init__('timer_printer')  # 调用父类 Node 的 __init__，参数是节点名
        self.count = 0                     # 自定义一个计数器，每次回调时 +1
        # 定时器：参数 1.0 = 间隔 1 秒，改成 0.5 则每秒触发两次
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):              # 定时器的回调函数，每次到时间就触发
        self.count += 1                    # 计数器 +1
        self.get_logger().info(            # ROS2 的日志输出，比 print() 更好用
            f'第 {self.count} 次 — 节点还活着！'  # f-string 格式化输出本次计数
        )


def main():                                # 主函数入口，ros2 run 实际执行的就是这个函数
    rclpy.init()                           # ① 初始化：整个进程只需调一次
    node = TimerPrinter()                  # ② 实例化节点：触发 __init__，启动定时器
    rclpy.spin(node)                       # ③ 进入循环：等待定时器触发，直到 Ctrl+C
    node.destroy_node()                    # ④ 销毁节点：释放资源（spin 结束后执行）
    rclpy.shutdown()                       # ⑤ 关机：关闭 ROS2 客户端


if __name__ == '__main__':                 # Python 标准入口：直接运行这个文件时才执行
    main()

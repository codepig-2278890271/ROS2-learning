"""参数回调演示 —— 监听参数变化，校验 + 实时响应

运行方式：
  ros2 run learning_parameter param_callback_demo
  # 然后在另一个终端里试：
  ros2 param set /param_callback_demo brightness 0.8    # 合法，生效
  ros2 param set /param_callback_demo brightness 1.5    # 不合法，拒绝
  ros2 param set /param_callback_demo exposure_mode "auto"
"""

from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
import rclpy


class ParamCallbackDemo(Node):
    """演示 add_on_set_parameters_callback —— 参数被改时自动触发"""

    def __init__(self):
        super().__init__('param_callback_demo')

        # ━━━ ① 声明参数 ━━━
        self.declare_parameter('brightness', 0.5)          # 亮度，0~1
        self.declare_parameter('contrast', 0.5)            # 对比度，0~1
        self.declare_parameter('exposure_mode', 'manual')  # 曝光模式

        # ━━━ ② 注册参数回调 —— 参数被 set 时自动触发 ━━━
        self.add_on_set_parameters_callback(self.on_param_changed)

        # ━━━ ③ 定时打印当前参数 ━━━
        self._timer = self.create_timer(2.0, self.print_params)

        self.get_logger().info('参数回调已注册，试试 ros2 param set 改参数')

    def on_param_changed(self, params: list[Parameter]) -> SetParametersResult:
        """参数被修改时自动调用。

        params 是被修改的参数列表（一次 set 可能改多个）。
        返回 SetParametersResult(successful=True/False) 告诉框架改没改成。
        """
        result = SetParametersResult(successful=True)

        for param in params:
            if param.name == 'brightness':
                # ── 校验：亮度必须在 0~1 ──
                if not 0.0 <= param.value <= 1.0:
                    result.successful = False
                    result.reason = '亮度必须在 0.0 ~ 1.0 之间'
                    self.get_logger().warn(f'❌ 拒绝参数改动: {result.reason}')
                    return result
                self.get_logger().info(f'✅ 亮度已更新: {param.value}')

            elif param.name == 'contrast':
                if not 0.0 <= param.value <= 1.0:
                    result.successful = False
                    result.reason = '对比度必须在 0.0 ~ 1.0 之间'
                    self.get_logger().warn(f'❌ 拒绝参数改动: {result.reason}')
                    return result
                self.get_logger().info(f'✅ 对比度已更新: {param.value}')

            elif param.name == 'exposure_mode':
                valid_modes = ['manual', 'auto', 'aperture_priority']
                if param.value not in valid_modes:
                    result.successful = False
                    result.reason = f'曝光模式必须是 {valid_modes} 之一'
                    self.get_logger().warn(f'❌ 拒绝参数改动: {result.reason}')
                    return result
                self.get_logger().info(f'✅ 曝光模式已更新: {param.value}')

        return result

    def print_params(self):
        """打印当前参数值"""
        b = self.get_parameter('brightness').value
        c = self.get_parameter('contrast').value
        m = self.get_parameter('exposure_mode').value
        self.get_logger().info(f'📷 亮度={b}  对比度={c}  曝光模式={m}')


def main():
    rclpy.init()
    rclpy.spin(ParamCallbackDemo())


if __name__ == '__main__':
    main()

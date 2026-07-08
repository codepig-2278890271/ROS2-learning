import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
from geometry_msgs.msg import Twist, Point


class PatrolRobot(Node):
    """
    巡逻机器人模拟器。

    行为：
      巡逻中(0) → 电量低于 20% → 返回中(1) → 到达充电站 → 充电中(2)
                                             → 电量回满 → 巡逻中(0)

    发布：/robot_pose    (Point)   当前位置
          /robot_status  (String)  状态信息
          /battery_level (Int32)   电量百分比

    订阅：/emergency_stop (Int32)   收到 1 立即急停
    """

    # 状态常量
    PATROLLING = 0      # 巡逻中
    RETURNING = 1       # 返回充电中
    CHARGING = 2        # 充电中

    STATE_LABEL = {0: '巡逻中', 1: '返回充电', 2: '充电中'}

    def __init__(self):
        super().__init__('patrol_robot')
        self.state = self.PATROLLING               # 当前状态

        # ━━━━ 参数（可调）━━━━
        self.declare_parameter('speed', 0.5)        # 移动速度（米/帧，一帧 1 秒）
        self.declare_parameter('battery_drain', 2)  # 每秒消耗电量 %
        self.declare_parameter('charge_rate', 5)    # 每秒充电量 %
        self.declare_parameter('low_battery', 20)   # 低电量阈值 %
        self.declare_parameter('update_rate', 1.0)  # 更新频率（秒），改小则移动更快、数据更密
        # ━━━━━━━━━━━━━━━━━━

        # 巡逻路径点（机器人围着这个矩形走）
        self.waypoints = [
            (0.0, 0.0),
            (5.0, 0.0),
            (5.0, 5.0),
            (0.0, 5.0),
        ]
        self.target_idx = 1                        # 当前目标路径点索引
        self.x, self.y = 0.0, 0.0                  # 当前位置
        self.battery = 100.0                       # 当前电量 %
        self.emergency = False                     # 急停标志

        # ━━━━ 发布者 ━━━━
        self.pose_pub = self.create_publisher(
            Point, '/robot_pose', 10               # Point 消息含 x, y, z 三个字段
        )
        self.status_pub = self.create_publisher(
            String, '/robot_status', 10
        )
        self.battery_pub = self.create_publisher(
            Int32, '/battery_level', 10
        )

        # ━━━━ 订阅者 ━━━━
        self.stop_sub = self.create_subscription(
            Int32, '/emergency_stop', self.emergency_callback, 10
        )

        # ━━━━ 主循环定时器 ━━━━
        self.timer = self.create_timer(
            self.get_parameter('update_rate').value,
            self.loop
        )

        self.get_logger().info('🤖 巡逻机器人已启动！')

    # ━━━━━━━ 回调 ━━━━━━━

    def emergency_callback(self, msg):
        if msg.data == 1 and not self.emergency:
            self.emergency = True
            self.get_logger().error('🚨 收到急停指令！机器人停止移动！')
        elif msg.data == 0 and self.emergency:
            self.emergency = False
            self.get_logger().warn('✅ 急停解除，恢复正常')

    # ━━━━━━━ 主循环 ━━━━━━━

    def loop(self):
        if self.emergency:
            self.publish_all()
            return

        if self.state == self.PATROLLING:
            self.patrol()
        elif self.state == self.RETURNING:
            self.return_to_charge()
        elif self.state == self.CHARGING:
            self.charge()

        self.publish_all()

    # ━━━━━━━ 状态行为 ━━━━━━━

    def patrol(self):
        """沿着巡逻路径点循环移动"""
        tx, ty = self.waypoints[self.target_idx]
        speed = self.get_parameter('speed').value
        drain = self.get_parameter('battery_drain').value

        # 向目标点移动
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)                  # 距离目标点还有多远

        if dist < speed:                            # 到达当前路径点
            self.x, self.y = tx, ty
            self.target_idx = (self.target_idx + 1) % len(self.waypoints)
            self.get_logger().info(
                f'📍 到达路径点 [{tx:.1f}, {ty:.1f}]，'
                f'下一目标 [{self.waypoints[self.target_idx][0]:.1f}, {self.waypoints[self.target_idx][1]:.1f}]'
            )
        else:                                       # 继续移动
            step = speed / dist
            self.x += dx * step
            self.y += dy * step

        self.battery -= drain
        self.get_logger().debug(f'位置: ({self.x:.2f}, {self.y:.2f}) | 电量: {self.battery:.0f}%')

        # 电量低 → 切换状态
        if self.battery <= self.get_parameter('low_battery').value:
            self.get_logger().warn(f'🔋 电量低 ({self.battery:.0f}%)，开始返回充电站！')
            self.state = self.RETURNING

    def return_to_charge(self):
        """驶回充电站 (0, 0)"""
        speed = self.get_parameter('speed').value
        drain = self.get_parameter('battery_drain').value

        dist = math.hypot(self.x, self.y)            # 距离充电站 (0,0) 的距离

        if dist < speed:                            # 到达充电站
            self.x, self.y = 0.0, 0.0
            self.get_logger().info('🔌 已到达充电站，开始充电！')
            self.state = self.CHARGING
        else:
            self.x -= (self.x / dist) * speed       # 向 (0,0) 移动
            self.y -= (self.y / dist) * speed
            self.battery -= drain
            self.get_logger().debug(f'返回中… 距离充电站 {dist:.2f}m | 电量: {self.battery:.0f}%')

    def charge(self):
        """充电"""
        charge_rate = self.get_parameter('charge_rate').value
        self.battery += charge_rate
        self.get_logger().info(f'⚡ 充电中… 当前电量: {self.battery:.0f}%')

        if self.battery >= 100.0:                   # 充满 → 回到巡逻
            self.battery = 100.0
            self.target_idx = 1                      # 从第二个路径点重新开始
            self.get_logger().info('🔋 充电完成，继续巡逻！')
            self.state = self.PATROLLING

    # ━━━━━━━ 发布 ━━━━━━━

    def publish_all(self):
        """一次性发布所有话题"""
        pose = Point()
        pose.x = self.x
        pose.y = self.y
        pose.z = 0.0
        self.pose_pub.publish(pose)

        status = String()
        status.data = f'state={self.STATE_LABEL[self.state]},battery={self.battery:.0f}%'
        self.status_pub.publish(status)

        battery_msg = Int32()
        battery_msg.data = int(self.battery)
        self.battery_pub.publish(battery_msg)


def main():
    rclpy.init()
    node = PatrolRobot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

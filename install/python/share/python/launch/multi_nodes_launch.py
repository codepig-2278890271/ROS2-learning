from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='python',
            executable='pub',
            name='py_publisher_node'
        ),
        Node(
            package='python',
            executable='sub',
            name='py_subscriber_node'
        ),
        Node(
            package='python',
            executable='turtle',
            name='turtle_control_node'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node'
        ),
    ])

import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/zhuzeyu/guyueju/ros2_21_tutorials/install/learning_gazebo'

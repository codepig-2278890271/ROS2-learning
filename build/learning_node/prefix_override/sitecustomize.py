import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/zhuzeyu/guyueju/ROS2-learning/install/learning_node'

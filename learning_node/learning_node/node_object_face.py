#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过Haar Cascade检测摄像头中的人脸，并用红框标出
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库

# 加载OpenCV自带的Haar级联人脸检测模型
face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')

def face_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                              # 转换为灰度图像

    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))       # 检测人脸

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)                # 用红色矩形框出人脸
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 0, 255), -1)         # 人脸中心点（红色）

    cv2.imshow("face", image)                                                    # 显示处理后的图像效果
    cv2.waitKey(50)

def main(args=None):                                                              # ROS2节点主入口main函数
    rclpy.init(args=args)                                                         # ROS2 Python接口初始化
    node = Node("node_object_face")                                               # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测摄像头中的人脸")

    cap = cv2.VideoCapture(0)

    while rclpy.ok():
        ret, image = cap.read()                                                   # 读取一帧图像

        if ret:
            face_detect(image)                                                    # 人脸检测

    cap.release()
    cv2.destroyAllWindows()
    node.destroy_node()                                                           # 销毁节点对象
    rclpy.shutdown()                                                              # 关闭ROS2 Python接口

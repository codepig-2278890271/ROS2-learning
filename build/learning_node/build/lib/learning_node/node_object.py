#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过颜色识别检测图片中出现的苹果
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库
import time                             # 时间库

lower_red = np.array([0, 90, 128])     # 红色的HSV阈值下限
upper_red = np.array([180, 255, 255])  # 红色的HSV阈值上限

def detect_freshness(hsv_img, mask, x, y, w, h):
    """
    检测苹果的新鲜度
    基于HSV中的饱和度(S)和亮度(V)来判断新鲜度
    """
    # 提取感兴趣区域(ROI)
    roi_hsv = hsv_img[y:y+h, x:x+w]
    roi_mask = mask[y:y+h, x:x+w]
    
    # 获取掩码内的像素
    valid_pixels = roi_hsv[roi_mask > 0]
    
    if len(valid_pixels) == 0:
        return "未知", 0
    
    # 计算平均饱和度和亮度
    avg_saturation = np.mean(valid_pixels[:, 1])
    avg_value = np.mean(valid_pixels[:, 2])
    
    # 新鲜度评分 (0-100)
    freshness_score = (avg_saturation / 255 * 0.6 + avg_value / 255 * 0.4) * 100
    
    # 根据评分判断新鲜度等级
    if freshness_score >= 70:
        freshness_level = "新鲜"
    elif freshness_score >= 50:
        freshness_level = "一般"
    else:
        freshness_level = "不新鲜"
    
    return freshness_level, freshness_score

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                               # 图像从BGR颜色模型转换为HSV模型
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)                          # 图像二值化

    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

    for cnt in contours:                                                          # 去除一些轮廓面积太小的噪声
        if cnt.shape[0] < 150:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                                      # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.drawContours(image, [cnt], -1, (255, 0, 0), 2)                        # 将苹果的轮廓勾勒出来（蓝色）
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (255, 0, 0), -1)           # 将苹果的图像中心点画出来（蓝色）
        
        # 检测苹果新鲜度
        freshness_level, freshness_score = detect_freshness(hsv_img, mask_red, x, y, w, h)
        print(f"检测到苹果：位置({x}, {y})，大小({w}x{h})，新鲜度：{freshness_level}，评分：{freshness_score:.1f}/100")
	    
    cv2.imshow("object", image)                                                    # 使用OpenCV显示处理后的图像效果
    
    # 持续显示窗口，只有Ctrl+C才能关闭
    try:
        while True:
            cv2.waitKey(100)  # 每100ms刷新一次
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()

def main(args=None):                                                              # ROS2节点主入口main函数
    rclpy.init(args=args)                                                         # ROS2 Python接口初始化
    node = Node("node_object")                                                     # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图片中的苹果")

    image = cv2.imread('/home/zhuzeyu/guyueju/ros2_21_tutorials/learning_node/learning_node/apple.jpg')  # 读取图像
    object_detect(image)                                                            # 苹果检测
    node.destroy_node()                                                            # 销毁节点对象
    rclpy.shutdown()                                                               # 关闭ROS2 Python接口

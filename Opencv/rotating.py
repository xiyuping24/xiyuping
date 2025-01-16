# import cv2 as cv
# img=cv.imread('picture.png')
# height,width=img.shape[:2]
# m=cv.getRotationMatrix2D((width/2,height/2),90,0.6)
# rotate=cv.warpAffine(img,m,(width,height))
# cv.imshow('1',img)
# cv.imshow('2',rotate)
# cv.waitKey()
# cv.destroyAllWindows()

import cv2
import numpy as np
import math

# 创建一个黑色的图像
hsv = np.zeros((400, 400, 3), dtype=np.uint8)

# 原始矩形的顶点，确保是浮点类型
rect_points = np.array([
    [200, 100],  # 左上
    [300, 200],  # 右上
    [250, 300],  # 右下
    [200, 300]   # 左下
], dtype=np.float32)  # 设定为浮点类型

# 计算矩形的质心
centroid = np.mean(rect_points, axis=0)

# 旋转角度（单位：度）
angle = 30

# 旋转矩阵计算
def rotate_point(point, angle, centroid):
    angle_rad = np.radians(angle)
    # 平移到原点
    point -= centroid
    # 旋转矩阵
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
    # 应用旋转
    rotated_point = np.dot(rotation_matrix, point)
    # 平移回原位置
    rotated_point += centroid
    return rotated_point

# 旋转矩形的四个顶点
rotated_points = np.array([rotate_point(p, angle, centroid) for p in rect_points])

# 将旋转后的矩形的顶点转换为整数
rotated_points = np.int32(rotated_points)

# 在图像上绘制原始矩形
cv2.polylines(hsv, [rect_points.astype(np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)

# 在图像上绘制旋转后的矩形
cv2.polylines(hsv, [rotated_points], isClosed=True, color=(0, 255, 0), thickness=2)

# 显示图像
cv2.imshow('Rotated Rectangle', hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

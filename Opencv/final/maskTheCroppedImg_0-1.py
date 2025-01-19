import cv2 as cv
import numpy as np
import os

def check(img):  # 判断蓝色区域是否是凸五边形
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 设置蓝色的HSV范围
    lower_blue = np.array([100, 70, 50])  # 低蓝色范围
    upper_blue = np.array([140, 255, 255])  # 高蓝色范围
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

    # 寻找蓝色区域的轮廓
    contours, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 计算轮廓的面积，如果面积过小则跳过
        area = cv.contourArea(contour)
        if area < 1000:  # 可以根据需求调整面积大小
            continue

        # 获取轮廓的近似多边形
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # 判断是否是五边形
        if len(approx) == 5:
            # 判断五边形是否为凸多边形
            if cv.isContourConvex(approx):
                # 绘制五边形
                cv.drawContours(img, [approx], -1, (0, 0, 255), 2)  # 红色标出五边形
                return True

    return False

# 指定图片所在的文件夹路径
input_folder = r'D:\pythonProject\image_0'  # 输入路径
output_folder = r'D:\pythonProject\image_1'  # 输出路径

# 获取文件夹中的所有文件
files = os.listdir(input_folder)

# 遍历文件夹中的每个文件
image_count = 1
for file in files:
    # 确保只处理图像文件，可以根据需要修改扩展名列表
    if file.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # 读取图片
        img_path = os.path.join(input_folder, file)
        img = cv.imread(img_path)

        if img is None:
            print(f"Error loading image: {file}")
            continue

        # --------------处理图像-------------------------#
        if check(img):  # 蓝色区域是凸五边形
            # 保存图像到新路径
            new_filename = f"image_{image_count:03d}.jpg"  # 自动编号，使用3位数
            new_filepath = os.path.join(output_folder, new_filename)

            # 保存图像
            cv.imwrite(new_filepath, img)
            print(f"Saved: {new_filepath}")

            # 增加计数
            image_count += 1
        # --------------处理图像-------------------------#

import cv2 as cv
import numpy as np
import os

# 处理每一张图像
def process_image(img):
    img = cv.resize(img, (480, 640))
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 蓝色范围
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    # mask_blue = cv.GaussianBlur(mask_blue, (5, 5), 0, 0)

    # 反转mask蓝色区域
    mask2 = 255 - mask_blue
    # mask2 = cv.GaussianBlur(mask2, (5, 5), 0, 0)

    # 阈值处理
    ret, binary = cv.threshold(mask_blue, 127, 255, cv.THRESH_BINARY)

    # 查找轮廓
    contours, hierarchy = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 灰度化图像
    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, img2 = cv.threshold(img2, 230, 255, cv.THRESH_TOZERO)

    # 轮廓填充白色
    img2 = cv.GaussianBlur(img2, (5, 5), 0, 0)
    whole_white = cv.drawContours(img2, contours, -1, (255, 255, 255), thickness=cv.FILLED)

    # 提取中间区域
    mid = cv.bitwise_and(mask2, whole_white)

    # 适应阈值操作
    img = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
    ret, adapt = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    adapt = cv.bitwise_and(mid, adapt)

    return adapt


# 批量处理图像并保存
def process_images(input_folder, output_folder):
    files = os.listdir(input_folder)

    # 创建输出路径，如果不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_count = 1  # 初始化图片计数器

    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # 确保只处理图像文件
            img_path = os.path.join(input_folder, file)
            img = cv.imread(img_path)

            if img is None:
                print(f"Error loading image: {file}")
                continue

            # 处理图像
            processed_img = process_image(img)

            # 自动编号并保存图像
            new_filename = f"image_{image_count:03d}.jpg"  # 使用3位数编号
            new_filepath = os.path.join(output_folder, new_filename)
            cv.imwrite(new_filepath, processed_img)
            print(f"Saved: {new_filepath}")

            image_count += 1  # 增加计数


# 设置输入路径和输出路径
input_folder = r'D:\pythonProject\image_2'  # 输入路径
output_folder = r'D:\pythonProject\image_3'  # 输出路径

# 批量处理图像
process_images(input_folder, output_folder)

import cv2 as cv
import numpy as np
import os

# 检测图像中的蓝色五边形
def detect_blue_polygon(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])  # 低蓝色范围
    upper_blue = np.array([140, 255, 255])  # 高蓝色范围
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        size = cv.contourArea(contour)
        if size < 1000:  # 可以调整面积阈值
            continue

        # 获取轮廓的近似多边形
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # 如果是五边形
        if len(approx) == 5:
            cv.drawContours(img, [approx], -1, (0, 0, 255), 2)  # 用红色画出五边形
            return approx  # 返回五边形的轮廓
    return None  # 没有找到五边形


# 计算五边形的角度并旋转图像
def rotate_to_up(img, approx):
    # 计算五边形的中心
    M = cv.moments(approx)
    if M["m00"] == 0:
        return img

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # 计算距离中心最远的点
    max_distance = 0
    farthest_point = None

    for point in approx:
        px, py = point[0]
        distance = np.sqrt((px - cx) ** 2 + (py - cy) ** 2)
        if distance > max_distance:
            max_distance = distance
            farthest_point = (px, py)

    # 计算中心到最远点的角度
    angle = np.arctan2(farthest_point[1] - cy, farthest_point[0] - cx) * 180 / np.pi

    # 旋转图像
    height, width = img.shape[:2]
    M = cv.getRotationMatrix2D((width / 2, height / 2), angle+90, 1)
    rotated_img = cv.warpAffine(img, M, (width, height))

    return rotated_img


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

            # 检测蓝色五边形并旋转图像
            approx = detect_blue_polygon(img)
            if approx is not None:
                rotated_img = rotate_to_up(img, approx)

                # 自动编号并保存图像
                new_filename = f"image_{image_count:03d}.jpg"  # 使用3位数编号
                new_filepath = os.path.join(output_folder, new_filename)
                cv.imwrite(new_filepath, rotated_img)
                print(f"Saved: {new_filepath}")

                image_count += 1  # 增加计数


# 设置输入路径和输出路径
input_folder = r'D:\pythonProject\image_1'  # 输入路径
output_folder = r'D:\pythonProject\image_2'  # 输出路径

# 批量处理图像
process_images(input_folder, output_folder)
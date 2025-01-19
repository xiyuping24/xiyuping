import cv2 as cv
import numpy as np
import os

# 处理每一张图像
def process_image(img):
    # img = cv.resize(img, (640, 640))
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 蓝色范围
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

    # 反转mask蓝色区域
    mask2 = 255 - mask_blue

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

# 通过掩码从原图裁剪出数字区域
def cutting2(adapt, ori_image):
    # 获取图像的高度和宽度
    height, width = ori_image.shape[:2]

    # 初始化裁剪图像为原图
    cropped = ori_image.copy()

    # 查找 adapt 区域的轮廓
    contours, _ = cv.findContours(adapt, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 获取轮廓的面积
        size = cv.contourArea(contour)
        if size < 100:  # 如果面积小于 100，跳过
            continue

        # 获取轮廓的最小外接矩形
        x, y, w, h = cv.boundingRect(contour)

        # 确保裁剪区域不会超出原图边界
        x = max(0, x)  # 防止x小于0
        y = max(0, y)  # 防止y小于0
        x_end = min(x + w, width)  # 防止x + w超出宽度
        y_end = min(y + h, height)  # 防止y + h超出高度

        # 从原图中截取指定区域
        cropped = ori_image[y:y_end, x:x_end]

    return cropped

def enhance(img):
    img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # 应用直方图均衡化
    equalized_image = cv.equalizeHist(img)
    return equalized_image

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
            ori = img  # 保存原图
            cv.imshow('ori', ori)
            # cv.waitKey()

            if img is None:
                print(f"Error loading image: {file}")
                continue

            # 处理图像
            processed_img = process_image(img)  # adapt
            # cv.waitKey()

            # 使用 adapt 图像从 ori 图像中裁剪相应的部分
            cropped_img = cutting2(processed_img, ori)
            height, width, channels = cropped_img.shape
            if height*width>5000 :
                continue
            if height*width<1000:
                continue
            # 自动编号并保存裁剪后的图像
            # kernel = np.ones((5, 5), np.uint8)
            # # 执行闭运算（先膨胀后腐蚀）
            # cropped_img = cv.morphologyEx(cropped_img, cv.MORPH_CLOSE, kernel) #黑色被当成噪点就更少了
            cropped=enhance(cropped_img)

            height,width=cropped.shape[:2]
            if max(height,width)/min(height,width)>1.5:
                continue
                        
            new_filename = f"image_{image_count:03d}.jpg"  # 使用3位数编号
            new_filepath = os.path.join(output_folder, new_filename)
            cv.imwrite(new_filepath, cropped)
            print(f"Saved: {new_filepath}")

            image_count += 1  # 增加计数

# 设置输入路径和输出路径
input_folder = r'image_2'  # 输入路径
output_folder = r'image_3'  # 输出路径

# 批量处理图像
process_images(input_folder, output_folder)


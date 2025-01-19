import cv2 as cv
import numpy as np
import os

# 初始化视频捕捉
cap = cv.VideoCapture('task4_level1.mov')  # 使用摄像头，传入视频文件路径可以处理视频文件
point = [0, 0]
i = 0  # 用于图片编号

# 确保目标文件夹存在
output_folder = r'D:\pythonProject\image_0'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为HSV空间
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 设置蓝色的HSV范围
    lower_blue = np.array([100, 120, 50])  # 低蓝色范围
    upper_blue = np.array([140, 255, 255])  # 高蓝色范围
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)


    def cutting(img, xx, yy):
        global i  # 使用全局变量i来编号
        l = 150
        x1 = max(xx - l, 0)  # 左上
        y1 = max(yy - l, 0)
        x2 = min(xx + l, img.shape[1])
        y2 = min(yy + l, img.shape[0])

        cropped = img[y1:y2, x1:x2]
        cv.imshow('cropped image', cropped)

        # 生成文件名，自动编号
        filename = f"cropped_{i:03d}.jpg"  # 例如 cropped_001.jpg, cropped_002.jpg
        filepath = os.path.join(output_folder, filename)

        # 保存裁剪后的图像
        cv.imwrite(filepath, cropped)

        # 更新编号
        i += 1


    def rotating(angle, mask_blue):
        rect = detect_contours(mask_blue, "Blue", 1)
        cv.imshow('1', frame)  # 原图

        height, width = frame.shape[:2]
        m = cv.getRotationMatrix2D((width / 2, height / 2), angle, 0.6)
        rotate = cv.warpAffine(frame, m, (width, height))
        hsv2 = cv.cvtColor(rotate, cv.COLOR_BGR2HSV)
        mask_blue2 = cv.inRange(hsv2, lower_blue, upper_blue)

        cv.imshow('test', mask_blue2)

        x = y = w = h = cx = cy = 0
        ang = 0
        contours, _ = cv.findContours(mask_blue2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            size = cv.contourArea(contour)
            if size < 100:
                continue
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 225, 0), 2)

            moments = cv.moments(contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

        print(x, y, w, h)
        point[0] = cx
        point[1] = cy
        print(point)
        print(w / h)
        print(x + w - point[0] - (point[0] - x))
        print(y + h - point[1] - (point[1] - y))
        cv.circle(rotate, (cx, cy), 81, (100, 100, 100), 4)

        if w / h > 1:
            if x + w - point[0] - (point[0] - x) < -10:
                ang += 90

            if x + w - point[0] - (point[0] - x) > 10:
                ang -= 90

        if w / h < 1:
            if y + h - point[1] - (point[1] - y) > 10:
                # print(1)
                ang = 180
            if y + h - point[1] - (point[1] - y) < -10:
                # print(1)
                ang = 0
        height, width = rotate.shape[:2]
        m = cv.getRotationMatrix2D((width / 2, height / 2), ang, 0.6)
        rotate = cv.warpAffine(rotate, m, (width, height))

        cv.imshow('2', rotate)
        cv.waitKey()


    # 对红色和蓝色掩码进行轮廓检测并扣出来
    def detect_contours(mask, color_name):
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            siz = cv.contourArea(contour)
            if 1500 < siz < 25000:  # 过滤掉大小不对的轮廓
                # 计算轮廓的矩形框
                x, y, w, h = cv.boundingRect(contour)
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 计算重心
                moments = cv.moments(contour)
                if moments["m00"] != 0:
                    cX = int(moments["m10"] / moments["m00"])
                    cY = int(moments["m01"] / moments["m00"])
                    # cv.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                    # cv.putText(frame, f'{color_name} center', (cX - 50, cY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                    #            (255, 255, 255), 2)

                    rect = cv.minAreaRect(contour)
                    point = rect[0]
                    print(point)
                    siz = rect[1]
                    print(siz)
                    angle = rect[2]
                    print(angle)
                    box = cv.boxPoints(rect)
                    box = np.int32(box)
                    cv.drawContours(frame, [box], 0, (0, 0, 255), 2)
                    cutting(frame, cX, cY)  # 调用cutting保存裁剪图像


    # 检测蓝色块
    detect_contours(mask_blue, "Blue")

    # 显示结果
    cv.imshow("Frame", frame)

    # 按 'q' 键退出
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv.destroyAllWindows()

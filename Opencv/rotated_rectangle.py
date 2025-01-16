import cv2
import numpy as np

# 初始化视频捕捉
cap = cv2.VideoCapture('task4_level1.mov')  # 使用摄像头，传入视频文件路径可以处理视频文件

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 设置红色的HSV范围
    # lower_red = np.array([0, 120, 120])  # 低红色范围
    # upper_red = np.array([10, 255, 255])  # 高红色范围
    # mask_red = cv2.inRange(hsv, lower_red, upper_red)
    #
    # lower_red2 = np.array([170, 120, 120])  # 红色另一部分范围
    # upper_red2 = np.array([180, 255, 255])
    # mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # 合并红色掩码
    # mask_red = cv2.bitwise_or(mask_red, mask_red2)

    # 设置蓝色的HSV范围
    lower_blue = np.array([100, 120, 50])  # 低蓝色范围
    upper_blue = np.array([140, 255, 255])  # 高蓝色范围
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)


    # 对红色和蓝色掩码进行轮廓检测
    def detect_contours(mask, color_name):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            siz=cv2.contourArea(contour)
            if 1000<siz<25000:  # 过滤掉大小不对的轮廓
                # 计算轮廓的矩形框
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 计算重心
                moments = cv2.moments(contour)
                if moments["m00"] != 0:
                    cX = int(moments["m10"] / moments["m00"])
                    cY = int(moments["m01"] / moments["m00"])
                    cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                    cv2.putText(frame, f'{color_name} center', (cX - 50, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)


                    rect = cv2.minAreaRect(contour)
                    point=rect[0]
                    print(point)
                    siz=rect[1]
                    print(siz)
                    angle=rect[2]
                    print(angle)
                    box = cv2.boxPoints(rect)
                    box=np.int32(box)
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

    # 检测红色和蓝色块
    # detect_contours(mask_red, "Red")
    detect_contours(mask_blue, "Blue")

    # 显示结果
    cv2.imshow("Frame", frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

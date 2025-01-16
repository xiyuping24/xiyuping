import cv2 as cv
cap=cv.VideoCapture(0)
#只有一个摄像头时默认0，就是电脑内置的摄像头

while(1):
    cap.set(cv.CAP_PROP_FPS, 10)
    ret,frame=cap.read();   #成功读取
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    cv.imshow('frame',gray)
    if cv.waitKey(1)&0xFF == ord('q'):
        #& 0xFF的按位与操作只取cv2.waitKey(1)返回值最后八位，有些系统cv2.waitKey(1)的返回值不止八位
        #窗口默认中文 换语言输入
        break
cap.release()
cv.destroyAllWindows()
#---------------------------------读电脑内置摄像头实时画面
# import cv2
# import numpy as np
# import cv2 as cv
#
# cap = cv.VideoCapture('tvideo.mp4')
#
# while(cap.isOpened()):
#     ret, frame = cap.read()
#
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#
#     cv.imshow('frame',gray)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv.destroyAllWindows()
#---------------------------------读出视频文件.mp4/.avi 好像没下载过ffmpeg/gstreamer

# import time
# t1=time.time()
# time.sleep(5)
# t2=time.time()
# print(t2-t1)
#---------------------------------python中时间函数等待与时间戳

# import numpy as np
# import cv2 as cv
#
# cap = cv.VideoCapture(0)
# fourcc = cv.VideoWriter_fourcc(*'XVID')   #用该编译器创建新视频文件
#out = cv.VideoWriter('output.avi',fourcc, 20.0, (640,480))
#创建的新文件名字  用于赋值的中间变量  帧率fps  (新的宽和高)
# while(cap.isOpened()):  #成功读取
#     ret, frame = cap.read()
#     if ret==True:
#         frame = cv.flip(frame,0)   #翻转图像
#
#         # write the flipped frame
#         out.write(frame)
#
#         cv.imshow('frame',frame)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# cap.release()
# out.release()
# cv.destroyAllWindows()
#-----------------------------------------保存视频

#----------------------修改函数----------------------------#
# change_video_resolution(input_video_path, output_video_path, new_width, new_height)
# frame = cv.flip(frame,0)   #翻转图像

# import cv2
# import numpy
#
# cap = cv2.VideoCapture(0)
#
# # 获取原视频的帧率
# fps = cap.get(cv2.CAP_PROP_FPS)
#
# # 创建视频写入对象
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('out_change_heightWidth.avi', fourcc, fps, (640, 480))
#
# while(1):
#     ret, frame = cap.read()
#
#     if not ret:
#         break
#
#     # 调整图像尺寸
#     resized_frame = cv2.resize(frame,(640, 480))
#
#     # 将调整后的帧写入输出视频文件
#     out.write(resized_frame)
#
#     # 显示当前帧（可选项）
#     cv2.imshow('Resizing Video', resized_frame)
#
#     # 按 'q' 键退出
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # 释放资源
# cap.release()
# out.release()
# cv2.destroyAllWindows()
#--------------------------改大小

# import cv2 as cv
# cap=cv.VideoCapture(0)
#
# cap.set(cv.CAP_PROP_FPS, 10);
# fourcc=cv.VideoWriter_fourcc(*'MJPG')
# out=cv.VideoWriter('output_changeFPS.mp4',fourcc,10,(620,480))
# while(1):
#     ret, frame=cap.read()
#     if not ret:
#         break
#     out.write(frame)
#     cv.imshow('modified',frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# out.release()
# cv.destroyAllWindows()
#---------------------------------改变帧率但是保存不下来avi/mp4
# import cv2 as cv
# import numpy as np
#
# img=cv.imread('layers.png')
# b=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# img1=cv.adaptiveThreshold(b,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,3)
# cv.imshow('test1',img1)
#
# contours,_=cv.findContours(img1,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
#
# hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
#
# lower_blue=np.array([100,50,50])
# upper_blue=np.array([140,255,255])
# mask_blue=cv.inRange(hsv,lower_blue,upper_blue)
#
#
#
# cv.imshow('test',mask_blue)
# cv.waitKey()

import cv2
import numpy as np
o=cv2.imread('layers.png')


hsv=cv2.cvtColor(o,cv2.COLOR_BGR2HSV)
lower_blue=np.array([100,50,50])
upper_blue=np.array([140,255,255])
mask_blue=cv2.inRange(hsv,lower_blue,upper_blue)
cv2.imshow("original",mask_blue)

# gray =cv2.cvtColor(o,cv2.COLOR_BGR2GRAY)

ret,binary=cv2.threshold(mask_blue,127,255,cv2.THRESH_BINARY)
contours, hierarchy=cv2.findContours(mask_blue,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

o = cv2.drawContours(o, contours, -1, (255, 255,255), thickness=cv2.FILLED)
cv2.imshow("result", o)
cv2.waitKey()
# for contour in contours:
#     size = cv2.contourArea(contour)
#     if size<100:
#         continue
#
#     for hie in hierarchy:
#         for h in hie:
#             if h[3] != -1:
#                 print(h)
#                 o=cv2.drawContours(o,contour,-1,(0,0,255),5)
#                 cv2.imshow("result",o)
#     cv2 .waitKey()
#     cv2 .destroyAllWindows()
#     print(hierarchy)
# ------------------------------常规显示蓝色轮廓


# import numpy as np
# import cv2 as cv
#
# img=cv.imread('bluearr.jpg')
# point=img[100,100]
# print(point)  # 彩色图返回RGB三个值
#
# img_gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# point2=img_gray[100,100]
# print(point2)  # 灰度图返回强度值img=cv.imread('bluearr.jpg')
#
#
# print(img.item(100,100,0))
# print(img.item(100,100,1))
# print(img.item(100,100,2))  # 更快

    # print(img_gray(100,100,1))  # 灰度图不行
#------------------------------------------------图像与数组

import numpy as np
import cv2 as cv

img=cv.imread('bluearr.jpg')
arr=img[200:300, 200:300]
img[300:400, 300:400]=arr
cv.imshow('test',img)
k=cv.waitKey()
if k==ord('q'):
    cv.destroyAllWindows()
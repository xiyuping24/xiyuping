# import cv2 as cv
#
# a=cv.imread('bluearr.jpg')
# b=cv.cvtColor(a,cv.COLOR_BGR2GRAY)
# cv.imshow('gray',b)
#
# k=cv.waitKey()
# if k==ord('c'):
#     c=cv.adaptiveThreshold(b,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,3)
#     cv.imshow('c',c)
#     k2=cv.waitKey()
#     if k2==ord('c'):
#         cv.destroyAllWindows()
#
# cv.destroyAllWindows()
#----------------------------------------------------------------------------自适应阈值处理

import cv2 as cv

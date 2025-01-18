# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
#
# img = cv.imread('picture.jpg',0)
# plt.hist(img.ravel(),256,[0,256]); plt.show()

# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# img = cv.imread('picture.jpg')
# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([img],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
# plt.show()
# 普通直方图与hsv直方图


import numpy as np
import cv2 as cv
img = cv.imread('picture.png',0)
# create a CLAHE object (Arguments are optional).
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv.imshow('ori',img)
cv.imshow('clahe_2.jpg',cl1)
cv.waitKey()
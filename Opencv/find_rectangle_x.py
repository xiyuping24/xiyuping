import cv2 as cv
import numpy as np

img=cv.imread('picture.jpg')
ret,thresh = cv.threshold(img,127,255,0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
M = cv.moments(cnt)
print( M )

x,y,w,h = cv.boundingRect(cnt)
cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
cv.imshow('test',img)
import cv2 as cv
import numpy as np

# img=cv.imread('picture.png')
cap=cv.VideoCapture('testVidoe.mp4')
while(1):

    ret,img=cap.read()

    if not ret:
        break

    img = cv.resize(img,(480,640))

    hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])  # 低蓝色范围
    upper_blue = np.array([140, 255, 255])  # 高蓝色范围
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask_blue=cv.GaussianBlur(mask_blue,(5,5),0,0)
    # cv.imshow('just blue',mask_blue)
    mask2=255-mask_blue
    mask2=cv.GaussianBlur(mask2,(5,5),0,0)
    # cv.imshow('mask_',mask2) #只有原蓝色区域是黑的，其余是白的

    ret,binary=cv.threshold(mask_blue,127,255,cv.THRESH_BINARY)

    contours, hierarchy=cv.findContours(mask_blue,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    img2=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    _,img2=cv.threshold(img2,230,255,cv.THRESH_TOZERO)

    cv.imshow('try',img)
    img2=cv.GaussianBlur(img2,(5,5),0,0)
    whole_white = cv.drawContours(img2, contours, -1, (255, 255,255), thickness=cv.FILLED)
    cv.imshow("result", whole_white)  # 蓝色以内区域全是白的

    mid=cv.bitwise_and(mask2,whole_white)
    cv.imshow("middle", mid) # 只有中间的白的

    img=cv.cvtColor(img,cv.COLOR_BGRA2GRAY)
    _,adapt=cv.threshold(img,127,255,cv.THRESH_BINARY)
    adapt=cv.bitwise_and(mid,adapt)
    adapt=cv.GaussianBlur(adapt,(5,5),0,0)
    cv.imshow('adapt',adapt)
    cv.waitKey()
    # if cv.waitKey(1) & 0xff == ord('q'):
    #     break


# cv.waitKey()
cap.release()
cv.destroyAllWindows()
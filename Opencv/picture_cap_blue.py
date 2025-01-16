import cv2 as cv
import numpy as np
import math

point=[0,0]
siz=[0,0]
angle=0

resized_frame=cv.imread('picture.png')
frame = cv.resize(resized_frame,(480,640))
hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)

lower_blue=np.array([100,50,50])
upper_blue=np.array([140,255,255])
mask_blue=cv.inRange(hsv,lower_blue,upper_blue)

def detect_contours(mask,color_name,op):
    contours,_=cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        size = cv.contourArea(contour)
        if size<100:
            continue
        x,y,w,h=cv.boundingRect(contour)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,225,0),2)

        # if op==2:
        #     arr=[x,y,w,h]
        #     return arr

        moments=cv.moments(contour)
        if moments["m00"]!=0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            cv.circle(frame,(cx,cy),7,(0,0,255),-1)
            cv.putText(frame, f'{color_name} center', (cx - 50, cy - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)

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
            return rect

rect=detect_contours(mask_blue, "Blue",1)
angle=rect[2]
cv.imshow('1',frame)
# 显示结果
# cv.imshow("Frame", frame)
# cv.imshow('test',mask_blue)
# cv.waitKey()


# rotate是正交的



# hsv=cv.cvtColor(rotate,cv.COLOR_BGR2HSV)
# mask_blue=cv.inRange(hsv,lower_blue,upper_blue)
# arr=detect_contours(mask_blue, "Blue",2)
# print(arr)

height,width=frame.shape[:2]
m=cv.getRotationMatrix2D((width/2,height/2),angle,0.6)
rotate=cv.warpAffine(frame,m,(width,height))
hsv2=cv.cvtColor(rotate,cv.COLOR_BGR2HSV)
mask_blue2=cv.inRange(hsv2,lower_blue,upper_blue)

cv.imshow('test',mask_blue2)


x=y=w=h=cx=cy=0
ang=0
contours,_=cv.findContours(mask_blue2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
for contour in contours:
    size = cv.contourArea(contour)
    if size<100:
        continue
    x,y,w,h=cv.boundingRect(contour)
    cv.rectangle(frame,(x,y),(x+w,y+h),(0,225,0),2)

    moments = cv.moments(contour)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

print(x,y,w,h)
point[0]=cx
point[1]=cy
print(point)
print(w/h)
print(x+w-point[0]-(point[0]-x))
print(y+h-point[1]-(point[1]-y))
cv.circle(rotate,(cx,cy),81,(100,100,100),4)

if w/h>1:
    if x+w-point[0]-(point[0]-x)<-10:
        ang+=90

    if x+w-point[0]-(point[0]-x)>10:
        ang-=90

if w/h<1:
    if y+h-point[1]-(point[1]-y)>10:
        # print(1)
        ang=180
    if y+h-point[1]-(point[1]-y)<-10:
        # print(1)
        ang=0
height,width=rotate.shape[:2]
m=cv.getRotationMatrix2D((width/2,height/2),ang,0.6)
rotate=cv.warpAffine(rotate,m,(width,height))
# point = rect[0]
# print(point)
# siz = rect[1]
# print(siz)
# w=siz[0]/2
# h=siz[1]/2
# lu=[point[0]-w,point[1]-h]
# lb=[point[0]-w,point[1]+h]
# ru=[point[0]+w,point[1]-h]
# rb=[point[0]+w,point[1]-h]
#

cv.imshow('2',rotate)
cv.waitKey()
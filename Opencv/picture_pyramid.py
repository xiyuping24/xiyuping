import cv2

# 读取图像
image = cv2.imread("apple.png")

# 构建图像金字塔
layer = image.copy()
for i in range(3):  # 如果原代码是 xrange(5)，改为 range(5)
    layer = cv2.pyrDown(layer)  # 降采样
    cv2.imshow(f"Layer {i+1}", layer)

cv2.waitKey(0)
cv2.destroyAllWindows()

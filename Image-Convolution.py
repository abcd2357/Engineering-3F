# -*- coding: utf-8 -*-
import cv2
import numpy as np

src = cv2.imread('STOP1.jpg')
# 灰度图像
src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 二值图像 黑 = 0 白 = 255
ret, src = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('src', src)

# 边缘保留
kernel = np.array([[-1, 2, -1],
                   [-1, 2, -1],
                   [-1, 2, -1]])
dst = cv2.filter2D(src, -1, kernel)
cv2.imshow('dst', dst)

# kernel设定

# 00100
# 00100
# 11111
# 00100
# 00100

kernel_2 = np.uint8(np.zeros((5, 5)))
for x in range(5):
    kernel_2[x, 2] = 1
    kernel_2[2, x] = 1

# 腐蚀图像
# dst = cv2.erode(dst, kernel_2)

# 膨胀图像
dst_2 = cv2.dilate(dst, kernel_2)

# 白黑互转
dst_2 = ~dst_2

cv2.imshow('dst_2', dst_2)
cv2.waitKey()
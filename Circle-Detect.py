# -*- coding: utf-8 -*-
import cv2
import numpy as np

img = cv2.imread('TRUESTOP.jpg')
# 灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# hough-transform

circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=35, minRadius=30, maxRadius=40)
# image为输入图像，需要灰度图。
# method为检测方法,常用CV2.HOUGH_GRADIENT。
# dp为检测内侧圆心的累加器图像的分辨率与输入图像之比的倒数，如dp=1，
# 累加器和输入图像具有相同的分辨率；如dp=2，累加器便有输入图像一半那么大的宽度和高度。
# minDist表示两个圆之间圆心的最小距离。
# param1有默认值100，它是method设置的检测方法的对应的参数，
# 对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT，它表示传递给canny边缘检测算子的高阈值，而低阈值为高阈值的一半。
# param2有默认值100，它是method设置的检测方法的对应的参数，
# 对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT，它表示在检测阶段圆心的累加器阈值，
# 它越小，就越可以检测到更多根本不存在的圆；它越大，能通过检测的圆就更加接近完美的圆形。
# minRadius有默认值0，圆半径的最小值；maxRadius有默认值0，圆半径的最大值。

circles = circles1[0, :, :] # 提取为二维
circles = np.uint16(np.around(circles)) # 四舍五入，取整

for i in circles[:]:
    cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 2) # 画圆
    cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 2) # 画圆心

print('The number of circles is:',len(circles1))
cv2.imshow('final', img)
cv2.waitKey()

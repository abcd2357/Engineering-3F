import cv2
import numpy as np

img = cv2.imread('Parking.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#BGR
low_1 = np.array([0, 0, 20])
high_1 = np.array([180, 110, 80])

low_2 = np.array([170, 150, 140])
high_2 = np.array([180, 200, 180])

low_3 = np.array([30, 200, 120])
high_3 = np.array([36, 255, 170])

low_4 = np.array([70, 140, 100])
high_4 = np.array([90, 230, 125])

n = input("Parking Num：")

if n == '1':
    mask_1 = cv2.inRange(hsv, low_1, high_1)
    cv2.imshow('1', ~mask_1)

if n == '2':
    mask_2 = cv2.inRange(hsv, low_2, high_2)
    cv2.imshow('2', ~mask_2)

if n == '3':
    mask_3 = cv2.inRange(hsv, low_3, high_3)
    cv2.imshow('3', ~mask_3)

if n == '4':
    mask_4 = cv2.inRange(hsv, low_4, high_4)
    cv2.imshow('4', ~mask_4)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()

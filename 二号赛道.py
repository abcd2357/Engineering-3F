# -*- coding: utf-8 -*-

# 20180623 XuKangyan

from driver import driver
import time
import cv2
import numpy as np

global cruise,error,number,area

cap = cv2.VideoCapture(1) #开摄像头,1前0后

def img_process():
    while(cap.isOpened()):
        mid = err = num = 0
        i = 1
        cru_1 = 'cruise_img/'+'1_cruise'+'.jpg' #二值化图像
        cru_2 = 'cruise_img/'+'origin'+'.jpg' #原图
        cru_4 = 'cruise_img/'+'4_dilated'+'.jpg' #处理后图像
        #cru_3 = 'cruise_img/'+'3_reverse'+'.jpg'
        #cru_5 = 'cruise_img/'+'STOP'+'.jpg'

        ret,cruise = cap.read() #ret值为True或False，代表有没有读到图像
        if ret == True:
            cruise = cv2.cvtColor(cruise,cv2.COLOR_BGR2GRAY) #灰度图像
            cruise = cv2.flip(cruise,-1) #翻转图像;0沿x轴翻转;>0沿y轴翻转;<0x,y轴同时翻转。
            cv2.imwrite(cru_2,cruise) #写入原图像

            # stop-sign detecting
            cir_det = cruise
            circles = cv2.HoughCircles(cir_det, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=35, minRadius=30, maxRadius=40)
            #cv2.imwrite(cru_5,cir_det)
            if circles is not None: num = len(circles)

            ret,cruise = cv2.threshold(cruise,120,255,cv2.THRESH_BINARY) #二值化,0黑1白
            cv2.imwrite(cru_1,cruise) #二值化图像写入

            # 图像卷积 留下垂直边缘
            kernel = np.array([[-1, 2, -1],
                               [-1, 2, -1],
                               [-1, 2, -1]])
            cruise = cv2.filter2D(cruise, -1, kernel)
            #cv2.imwrite(cru_3,~cruise)

            # 5*5方形（白）腐蚀or膨胀
            kernel_2 = np.uint8(np.zeros((5,5)))
            for x in range(5):
                kernel_2[x,x]=1

            cruise = cv2.dilate(cruise,kernel_2) #膨胀图像
            cruise = ~cruise #转为所巡线为黑色的图像
            cv2.imwrite(cru_4,cruise) #处理后图像写入

            #取下方41行
            for n in range(440,480,1):
                for j in range(30,610,1):
                    if cruise[n][j] == 0:
                        mid = mid + j
                        i = i + 1
                err = err + (mid/i - 320)

        err = err/41
        err = int(err)
        print('error get: ', err)
        break
    return err,num,i

def main():
    print("========== piCar Client Start ==========")
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="speed")

    print("========== Cruise Start ==========")
    #d.setStatus(mode="speed")

    # 巡线
    while True:
        img_process()
        error,number,area = img_process()

        if(area > 200): #循线轨迹可探测
            st = error * 0.005
        else:
            st = error * 0.05 #舵机打满

        d.setStatus(motor = 0.04, servo = -st, dist=0x00, mode="speed") #循线主代码
        print("The Servo is: ", -st)

    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    cap.release()
    print("========== Cruise Stop ==========")


    print("========== Parking Start ==========")
    cappark = cv2.VideoCapture(0)
    n = input("Parking Number? ：")

    # hsv阈值参数
    low_1 = np.array([75, 90, 60])
    high_1 = np.array([130, 180, 130])

    low_2 = np.array([145, 90, 60])
    high_2 = np.array([200, 255, 255])

    low_3 = np.array([25, 145, 105])
    high_3 = np.array([40, 260, 185])

    low_4 = np.array([55, 65, 25])
    high_4 = np.array([95, 255, 135])

    while(cappark.isOpened()):

        ret,park = cappark.read()

        parking = 'cruise_img/'+'parking'+'.jpg'
        cv2.imwrite(parking, park) #停车原图写入

        hsvp = cv2.cvtColor(park, cv2.COLOR_BGR2HSV)
        i = j = x = dis = 0
        m = 1

        if n == '1':
            mask_1 = cv2.inRange(hsvp, low_1, high_1)
            maskp = ~mask_1
        if n == '2':
            mask_2 = cv2.inRange(hsvp, low_2, high_2)
            maskp = ~mask_2
        if n == '3':
            mask_3 = cv2.inRange(hsvp, low_3, high_3)
            maskp = ~mask_3
        if n == '4':
            mask_4 = cv2.inRange(hsvp, low_4, high_4)
            maskp = ~mask_4

        for i in range(639):
            for j in range(479):
                if maskp[j][i] == 0:
                    x = x+i
                    m = m+1

        park_mask = 'cruise_img/'+'park_mask'+'.jpg'
        cv2.imwrite(park_mask, maskp) #停车处理图像写入

        x = int(x/m)
        dis = 320 - x
        print("Parking ", n, "'s X is: ", x)
        print("dis is: ", dis, "m is: ", m )

        # bang-bang control
        if dis < 0 :
            if dis > -50 :
                d.setStatus(motor=-0.5, servo=0.0, dist=0xA0, mode="distance") # 直走
                print("Left Ahead")
            else :
                d.setStatus(motor=-0.6, servo=1, dist=0xA0, mode="distance")
                print("Left Trend")
        else:
            if dis < 50 :
                d.setStatus(motor=-0.5, servo=0.0, dist=0xA0, mode="distance") # 直走
                print("Right Ahead")
            else :
                d.setStatus(motor=-0.6, servo=-1, dist=0xA0, mode="distance")
                print("Right Trend")

        if m > 6000 :  # 足够接近车库
            break

        '''
        #另一种停车方式：P调节 control

        st = dis * 0.015

        if((dis > 120)or(dis < -120)):
            d.setStatus(motor= -0.5, servo= -st, dist=0xA0, mode="distance")
        else:
            d.setStatus(motor= -0.5, servo=0, dist=0xA0, mode="distance") #直行

        if (m > 4000):  # 足够接近车库
            break
        '''

    d.setStatus(motor=-0.2, servo=0.0, dist=0xFF0, mode="distance")
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    print("========== Parking Is Over ==========")
    cappark.release()

    d.close()
    del d

    print("========== piCar Client Fin ==========")
    return 0

if __name__ == '__main__':
    main()

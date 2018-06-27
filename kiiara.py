import cv2
import numpy as np
#import  imutils
import sys
import pytesseract
from PIL import Image
import json
#import show
img_org = cv2.imread(sys.argv[1])
#img_org = cv2.resize(img_org,None,fx=1/2,fy=1/2,interpolation=cv2.INTER_CUBIC)
img_bw = cv2.cvtColor(img_org , cv2.COLOR_BGR2GRAY)

for num in range(50,255):
	ret3,img_thr = cv2.threshold(img_bw,num,255,cv2.THRESH_BINARY)
#	cv2.imwrite('thresh.jpg',img_thr)

	img_edg  = cv2.Canny(img_thr ,100,200)

#	cv2.imwrite('cn_edge.jpg' , img_edg)



	kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (7, 7))
	img_dil = cv2.dilate(img_edg, kernel, iterations = 1)

#	cv2.imwrite('dilated_img.jpg',img_dil)


	#if  you  are  using  opencv 2.X then  make  sure  to  remove  "something_else " variable  from  list  below

	(somethig_else,contours ,hierarchye) = cv2.findContours(img_dil.copy(), 1, 2)
	cnts = sorted(contours, key = cv2.contourArea, reverse = True)

	screenCnt = None

	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points, then
		# we can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break





	mask = np.zeros(img_bw.shape, dtype=np.uint8)
	roi_corners = np.array(screenCnt ,dtype=np.int32)
	roi_corners = []
	ignore_mask_color = (255,)*1
	cv2.fillPoly(mask, roi_corners , ignore_mask_color)
	cv2.drawContours(img_org, [screenCnt], -40, (100, 255, 100), 9)
	#cv2.imshow('original  image with boundry' , img_org)
	cv2.imwrite('plate_detedted.jpg',img_org)


	ys =[screenCnt[0,0,1] , screenCnt[1,0,1] ,screenCnt[2,0,1] ,screenCnt[3,0,1]]
	xs =[screenCnt[0,0,0] , screenCnt[1,0,0] ,screenCnt[2,0,0] ,screenCnt[3,0,0]]

	ys_sorted_index = np.argsort(ys)
	xs_sorted_index = np.argsort(xs)

	x1 = screenCnt[xs_sorted_index[0],0,0]
	x2 = screenCnt[xs_sorted_index[3],0,0]

	y1 = screenCnt[ys_sorted_index[0],0,1]
	y2 = screenCnt[ys_sorted_index[3],0,1]



	img_plate = img_org[y1:y2 , x1:x2]

	# for i in screenCnt:
	#     print(i)
	#
	# print xs , ys
	#
	# print x1,x2,y1,y2
	#cv2.imshow('number plate',img_plate)

#	cv2.imwrite('number_plate.jpg',img_plate)
	img_plate_bw=cv2.cvtColor(img_plate,cv2.COLOR_BGR2GRAY)
	a,gr=cv2.threshold(img_plate_bw,160,200,cv2.THRESH_BINARY)
	a=cv2.medianBlur(gr,1)
#	cv2.imshow('HAHAH',a)
	#cv2.imwrite('denoised-{}.png'.format(num),a)
	ret,thrashed = cv2.threshold(a,220,250,cv2.THRESH_BINARY)
#	cv2.imshow('ddd',thrashed)
#	cv2.imwrite('aaa.png',thrashed)
	b=cv2.bitwise_not(a)
#	cv2.imshow('HAHAH',b)
	text=pytesseract.image_to_string(a)
	d={}
	if(text):
		print(num)
		print(text)
		pass
		#submitdata(text)
#	print(text)
#	print(text)
#	cv2.waitKey(0)


# Smart India Hackathon 2018 (Highway and road ministry)
Project for Smart India Hackathon 2018

This code (kiiara.py) detects the number plate in an image and converts it to text. 
The image is sent to the code as a command line argument.

Usage : python kiiara.py <image_name>

The code is sensitive to lighting conditions a for loop is used which iterates over the different luminious values ranging from 50-255.
You may get rid of the for loop and use particular range. In order to do that. change the line cv2.threshold(img_bw,num,255,cv2.THRESH_BINARY)
to cv2.threshold(img_bw,a,b,cv2.THRESH_BINARY) where a<b and a,b lies between 0 and 255. as pytesseract is succeptible to noise so use better 
blurring algorithm (gaussian blur is used  in this case)

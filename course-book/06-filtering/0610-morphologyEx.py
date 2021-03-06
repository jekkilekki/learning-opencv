# 0610.py
import cv2 
import numpy as np

src = cv2.imread('../../img/shapes.png', cv2.IMREAD_GRAYSCALE)
kernel = cv2.getStructuringElement(shape = cv2.MORPH_RECT, ksize = (3,3))
closing = cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel, iterations = 5)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations = 5)
gradient = cv2.morphologyEx(opening, cv2.MORPH_GRADIENT, kernel)
# gradient = cv2.morphologyEx(opening, cv2.MORPH_GRADIENT, kernel, iterations = 5)

tophat = cv2.morphologyEx(src, cv2.MORPH_TOPHAT, kernel, iterations = 5)
blackhat = cv2.morphologyEx(src, cv2.MORPH_BLACKHAT, kernel, iterations = 5)

cv2.imshow('opening', opening) # think of as "dilate"
cv2.imshow('closing', closing) # think of as "erode"
cv2.imshow('gradient', gradient) # where does the pixel vector (gradient) change? finds the lines
cv2.imshow('tophat', tophat) # find all the "salt"
cv2.imshow('blackhat', blackhat) # find all the "pepper"

cv2.waitKey()
cv2.destroyAllWindows()
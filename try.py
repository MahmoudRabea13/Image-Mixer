import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
mat = cv.imread('./tobeuploaded/camera.jpg')
mat = cv.cvtColor(mat, cv.COLOR_BGR2GRAY)
fou = np.fft.fft2(mat)
fou = np.fft.fftshift(fou)
fou[100:200,100:200] = 0
# cv.imshow('hello',np.log(np.angle(fou)))
invo = np.fft.ifft2(fou)
cv.imshow('hello',invo)
# cv.imshow('hello',mat)
cv.waitKey(0)
cv.destroyAllWindows()
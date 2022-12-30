import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
class Functions():
    fourier_1 = []
    fourier_2 = []
    def fourier(img):
        matrix = cv.imread(img)
        matrix = cv.cvtColor(matrix, cv.COLOR_BGR2GRAY)
        fourier = np.fft.fft2(matrix)
        fourier = np.fft.fftshift(fourier)
        return fourier
    def magphase(fourier, select):
        if select == 'mag':
            return np.abs(fourier)
        elif select == 'phase':
            return np.angle(fourier)
    def cut(fourier, x, y,width, height, select):
        if select == 'cut':
            cut_mat = np.ones((fourier.shape[0], fourier.shape[1]))
            cut_mat[y:y+height,x:x+width] = 0
        elif select == 'keep':
            cut_mat = np.zeros((fourier.shape[0], fourier.shape[1]))
            cut_mat[y:y+height,x:x+width] = 1
        return fourier*cut_mat
    def visulaize(fourier,number):
        plt.figure()
        plt.imshow(fourier, cmap='gray')
        plt.savefig(f'static/{number}.jpg')
    def re_fourier(magnitude,phase):
        re_fourier = magnitude*np.exp(1j*phase)
        re_fourier = np.fft.ifft2(re_fourier)
        return re_fourier
    
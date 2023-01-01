import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
class Functions():
    fourier_1 = []
    fourier_2 = []
    # fou_send_1 = []
    # fou_send_2 = []
    cut_or_keep = 0
    cutting_mat = []
    # ,[0,100,100,100,100,0],[0,400,400,300,300,0]
    # ,[1,100,600,10,10],[1,200,200,50,50],[1,600,400,200,100]
    temp_fourier_1 = np.zeros((800,800))
    temp_fourier_2 = np.zeros((800,800))
    var = [0,3]
    flag_1 = False
    flag_2 = False
    random_mat = np.random.randint(0,1000,size=(800,800))
    fouriers_list = [random_mat,random_mat,random_mat,random_mat]
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
        plt.axis('off')
        plt.savefig(f'static/{number}.jpg', bbox_inches='tight', pad_inches=0)
    def re_fourier(magnitude,phase):
        re_fourier = magnitude*np.exp(1j*phase)
        re_fourier = np.fft.ifft2(re_fourier)
        return re_fourier
    
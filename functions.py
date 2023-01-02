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
    def cut(fourier, list_dimensions):
        if list_dimensions[0] == 1:
            cut_mat = np.ones((fourier.shape[0], fourier.shape[1]))
            cut_mat[list_dimensions[2]:list_dimensions[2]+list_dimensions[4],list_dimensions[1]:list_dimensions[1]+list_dimensions[3]] = 0
        elif list_dimensions[0] == 0:
            cut_mat = np.zeros((fourier.shape[0], fourier.shape[1]))
            cut_mat[list_dimensions[2]:list_dimensions[2]+list_dimensions[4],list_dimensions[1]:list_dimensions[1]+list_dimensions[3]] = 1
        return fourier*cut_mat
    def visulaize(fourier,number):
        plt.figure()
        plt.imshow(fourier, cmap='gray')
        plt.axis('off')
        plt.savefig(f'static/{number}.jpg', bbox_inches='tight', pad_inches=0)
    def mix_fourier(magnitude,phase):
        re_fourier = magnitude*np.exp(1j*phase)
        re_fourier= np.fft.ifftshift(re_fourier)
        re_fourier = np.fft.ifft2(re_fourier)
        return re_fourier
    def dimension(list_of_dim):
        for i in range(len(list_of_dim)):
            for j in range(len(list_of_dim[i])):
                list_of_dim[i][j] = int(list_of_dim[i][j]*800/369)
        return list_of_dim
    def json_to_list(list_of_data):
        if len(list_of_data) > 4:
            if list_of_data[0] == None:
                cutting_list = [[],list_of_data[4:]]
            else:
                cutting_list = [list_of_data[:4],list_of_data[4:]]
        else:
            cutting_list = [list_of_data[:4],[]]
        return cutting_list
    def append_state(selection,item,list_of_data):
        phase_falg = True
        for i in range(len(list_of_data)):
            list_of_data[i].insert(0,selection)
            if item == 0 and phase_falg:
                list_of_data[i].append(1)
                phase_falg = False
            else:
                list_of_data[i].append(0)
        return list_of_data
    def show_image(order):
        order_list = [[1,2],[],[2,1]]
        Functions.visulaize(np.log(Functions.fouriers_list[Functions.var[0]]),order_list[order][0])
        Functions.visulaize(Functions.fouriers_list[Functions.var[1]],order_list[order][1])
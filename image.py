import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
class Image():
    fourier_1 = []
    fourier_2 = []
    cut_or_keep = 0
    cutting_mat = []
    temp_fourier_1 = np.zeros((800,800))
    temp_fourier_2 = np.zeros((800,800))
    var = [0,3]
    uni_mat = np.random.uniform(size=(800,800))
    fouriers_list = [uni_mat,uni_mat,uni_mat,uni_mat]
    def set_Fourier(Fourier,number):
        if number == 1:
            Image.fourier_1 = Fourier
        elif number == 2:
            Image.fourier_2 = Fourier
    def get_Fourier(Fourier,number):
        if number == 1:
            return Image.fourier_1
        elif number == 2:
            return Image.fourier_2
    def set_cut_or_keep(cut_or_keep):
        Image.cut_or_keep = cut_or_keep
    def get_cut_or_keep():
        return Image.cut_or_keep
    def set_cutting_mat(cutting_mat):
        Image.cutting_mat = cutting_mat
    def get_cutting_mat():
        return Image.cutting_mat
    def set_temp_fourier_1(temp_fourier,number):
        if number == 1:
            Image.temp_fourier_1 = temp_fourier
        elif number == 2:
            Image.temp_fourier_2 = temp_fourier
    def get_temp_fourier_1():
        return Image.temp_fourier_1
        
        
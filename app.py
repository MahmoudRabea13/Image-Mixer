from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import json
from flask import jsonify
from functions import *
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')
# @app.route('/get', methods=['GET', 'POST'])
# def get(jsdata):
#     print(jsdata)
#     return 'success'
# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     print('hello')
#     print(request.form['data'])
#     return 'success'
# if __name__ == '__main__':
#     app.run()

########################################### Misara #######################################
r = 0
@app.route("/" ,methods=['POST','GET'])
def image():
    if request.method == 'POST':
        img1=request.files.get('image1')
        img2=request.files.get('image2')
        phasemag = request.files.get('phasemag')
        select_cut = request.files.get('selectORcut')
        try:
            r = request.get_json()
            list_of_data = r['data']
            if len(list_of_data)>6 and list_of_data[1] == None:
                for i in range(4):
                    list_of_data[i] = 0
            for i in range(len(list_of_data)):
                list_of_data[i] = int(list_of_data[i]*800/369)
            list_of_data.insert(0,Functions.cut_or_keep)
            if Functions.var[0] == 0:
                if list_of_data[3]==0:
                    list_of_data.insert(5,Functions.cut_or_keep)
                    list_of_data.append(0)
                    Functions.cutting_mat = [list_of_data[5:]]
                    print(Functions.cutting_mat)
                else:
                    if len(list_of_data)>6:
                        list_of_data.insert(5,1)
                        list_of_data.insert(6,Functions.cut_or_keep)
                        list_of_data.append(0)
                        Functions.cutting_mat = [list_of_data[:6],list_of_data[6:]]
                        print(Functions.cutting_mat)
                    if len(list_of_data) <= 6:
                        list_of_data.append(1)
                        Functions.cutting_mat = [list_of_data[:6]]
                        print(Functions.cutting_mat)    
            else:
                if list_of_data[4]==0:
                    list_of_data.insert(5,Functions.cut_or_keep)
                    list_of_data.append(0)
                    Functions.cutting_mat = [list_of_data[5:]]
                    print(Functions.cutting_mat)
                else:
                    if len(list_of_data)>6:
                        list_of_data.insert(5,0)
                        list_of_data.insert(6,Functions.cut_or_keep)
                        list_of_data.append(1)
                        Functions.cutting_mat = [list_of_data[:6],list_of_data[6:]]
                        print(Functions.cutting_mat)
                    if len(list_of_data) <= 6:
                        list_of_data.append(0)
                        Functions.cutting_mat = [list_of_data[:6]]
                        print(Functions.cutting_mat) 
        except:
            Functions.cutting_mat = [[0,0,0,800,800,1]]
            print('hello')
            pass
        if select_cut != None:
            if select_cut.filename == '1':
                Functions.cut_or_keep = 0
            else:
                Functions.cut_or_keep = 1         
        if phasemag != None:
            if phasemag.filename == '1':
                Functions.var = [2,1]
            else:
                Functions.var = [0,3]
        if img1 != None:
            imgs_save = img1.filename + '.jpg'
            img1.save(imgs_save)
            Functions.fourier_1 = Functions.fourier('./image1.jpg')
            Functions.fouriers_list[0] = Functions.magphase(Functions.fourier_1, 'mag')
            Functions.fouriers_list[1] = Functions.magphase(Functions.fourier_1, 'phase')
            Functions.flag_1 = True
        if img2 != None:
            imgs_save2 = img2.filename + '.jpg'
            img2.save(imgs_save2)
            Functions.fourier_2 = Functions.fourier('./image2.jpg')
            Functions.fouriers_list[2] = Functions.magphase(Functions.fourier_2, 'mag')
            Functions.fouriers_list[3] = Functions.magphase(Functions.fourier_2, 'phase')
            Functions.flag_2 = True
        Functions.temp_fourier_1 = Functions.fouriers_list[Functions.var[0]]
        Functions.temp_fourier_2 = Functions.fouriers_list[Functions.var[1]]
        for i in range(len(Functions.cutting_mat)):
            if Functions.cutting_mat[i][5] == 0:
                if Functions.cutting_mat[i][0] == 0:
                    Functions.temp_fourier_2 = Functions.cut(Functions.temp_fourier_2,Functions.cutting_mat[i][1],Functions.cutting_mat[i][2],Functions.cutting_mat[i][3],Functions.cutting_mat[i][4],'keep')
                if Functions.cutting_mat[i][0] == 1:
                    Functions.temp_fourier_2 = Functions.cut(Functions.temp_fourier_2,Functions.cutting_mat[i][1],Functions.cutting_mat[i][2],Functions.cutting_mat[i][3],Functions.cutting_mat[i][4],'cut')
            if Functions.cutting_mat[i][5] == 1:
                if Functions.cutting_mat[i][0] == 0:
                    Functions.temp_fourier_1 = Functions.cut(Functions.fouriers_list[Functions.var[0]],Functions.cutting_mat[i][1],Functions.cutting_mat[i][2],Functions.cutting_mat[i][3],Functions.cutting_mat[i][4],'keep')
                if Functions.cutting_mat[i][0] == 1:
                    Functions.temp_fourier_1 = Functions.cut(Functions.fouriers_list[Functions.var[0]],Functions.cutting_mat[i][1],Functions.cutting_mat[i][2],Functions.cutting_mat[i][3],Functions.cutting_mat[i][4],'cut')
        # Functions.fouriers_list[Functions.var[0]] =  Functions.temp_fourier_2   
        if Functions.var[0] == 0:
            Functions.visulaize(np.log(Functions.fouriers_list[Functions.var[0]]),1)
            Functions.visulaize(Functions.fouriers_list[Functions.var[1]],2)
        elif Functions.var[0] == 2:
            Functions.visulaize(np.log(Functions.fouriers_list[Functions.var[0]]),2)
            Functions.visulaize(Functions.fouriers_list[Functions.var[1]],1)
        re_image = Functions.re_fourier(Functions.temp_fourier_1,Functions.temp_fourier_2)
        Functions.visulaize(np.abs(re_image),3)
        return render_template('main.html')
    else:
        return render_template('main.html')
if __name__ == '__main__':
    app.run(debug=True)
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
            new_list = Functions.json_to_list(list_of_data)
            new_list = Functions.dimension(new_list)
            new_list = Functions.append_state(Functions.cut_or_keep,Functions.var[0],new_list)
            Functions.cutting_mat = new_list
        except:
            Functions.cutting_mat =[[],[]]
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
        if img2 != None:
            imgs_save2 = img2.filename + '.jpg'
            img2.save(imgs_save2)
            Functions.fourier_2 = Functions.fourier('./image2.jpg')
            Functions.fouriers_list[2] = Functions.magphase(Functions.fourier_2, 'mag')
            Functions.fouriers_list[3] = Functions.magphase(Functions.fourier_2, 'phase')
        Functions.temp_fourier_1 = Functions.fouriers_list[Functions.var[0]]
        Functions.temp_fourier_2 = Functions.fouriers_list[Functions.var[1]]
        for i in range(len(Functions.cutting_mat)):
            if len(Functions.cutting_mat[i]) > 2:
                if Functions.cutting_mat[i][5]==0:
                    Functions.temp_fourier_2 =  Functions.cut(Functions.fouriers_list[Functions.var[1]],Functions.cutting_mat[i][:5])
                else:
                    Functions.temp_fourier_1 = Functions.cut(Functions.fouriers_list[Functions.var[0]],Functions.cutting_mat[i][:5])
        Functions.show_image(Functions.var[0])
        re_image = Functions.mix_fourier(Functions.temp_fourier_1,Functions.temp_fourier_2)
        Functions.visulaize(np.abs(re_image),3)
        return render_template('main.html')
    else:
        return render_template('main.html')
if __name__ == '__main__':
    app.run(debug=True)
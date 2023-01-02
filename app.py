from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import json
from flask import jsonify
from functions import *
from image import *
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
            new_list = Functions.append_state(Image.cut_or_keep,Image.var[0],new_list)
            Image.cutting_mat = new_list
        except:
            Image.cutting_mat =[[],[]]
        if select_cut != None:
            if select_cut.filename == '1':
                Image.cut_or_keep = 0
            else:
                Image.cut_or_keep = 1         
        if phasemag != None:
            if phasemag.filename == '1':
                Image.var = [2,1]
            else:
                Image.var = [0,3]
        if img1 != None:
            imgs_save = img1.filename + '.jpg'
            img1.save(imgs_save)
            Image.fourier_1 = Functions.fourier('./image1.jpg')
            Image.fouriers_list[0] = Functions.magphase(Image.fourier_1, 'mag')
            Image.fouriers_list[1] = Functions.magphase(Image.fourier_1, 'phase')
        if img2 != None:
            imgs_save2 = img2.filename + '.jpg'
            img2.save(imgs_save2)
            Image.fourier_2 = Functions.fourier('./image2.jpg')
            Image.fouriers_list[2] = Functions.magphase(Image.fourier_2, 'mag')
            Image.fouriers_list[3] = Functions.magphase(Image.fourier_2, 'phase')
        Image.temp_fourier_1 = Image.fouriers_list[Image.var[0]]
        Image.temp_fourier_2 = Image.fouriers_list[Image.var[1]]
        for i in range(len(Image.cutting_mat)):
            if len(Image.cutting_mat[i]) > 2:
                if Image.cutting_mat[i][5]==0:
                    Image.temp_fourier_2 =  Functions.cut(Image.fouriers_list[Image.var[1]],Image.cutting_mat[i][:5])
                else:
                    Image.temp_fourier_1 = Functions.cut(Image.fouriers_list[Image.var[0]],Image.cutting_mat[i][:5])
        Functions.show_image(Image.var[0])
        re_image = Functions.mix_fourier(Image.temp_fourier_1,Image.temp_fourier_2)
        Functions.visulaize(np.abs(re_image),3)
        return render_template('main.html')
    else:
        return render_template('main.html')
if __name__ == '__main__':
    app.run(debug=True)
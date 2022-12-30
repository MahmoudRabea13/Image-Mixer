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


@app.route("/" ,methods=['POST','GET'])
def image():
    if request.method == 'POST':
        img1=request.files.get('image1')
        img2=request.files.get('image2')
        phasemag = request.files.get('phasemag')
        select_cut = request.files.get('selectORcut')
        if select_cut != None:
            if select_cut.filename == '1':
                print('select')
            else:
                print('CUTZZZZZ')            
        if phasemag != None:
            if phasemag.filename == '1':
                print('phase1mag2')
            else:
                print('phase2mag1')
        if img1 != None:
            imgs_save = img1.filename + '.jpg'
            img1.save(imgs_save)
            Functions.fourier_1 = Functions.fourier('./image1.jpg')
            Functions.fourier_1 = Functions.magphase(Functions.fourier_1, 'mag')
            Functions.visulaize(np.log(Functions.fourier_1),1)
            Functions.flag_1 = True
        if img2 != None:
            imgs_save2 = img2.filename + '.jpg'
            img2.save(imgs_save2)
            Functions.fourier_2 = Functions.fourier('./image2.jpg')
            Functions.fourier_2 = Functions.magphase(Functions.fourier_2, 'phase')
            Functions.visulaize(Functions.fourier_2,2)
            Functions.flag_2 = True
        if Functions.flag_1:
            re_image = Functions.re_fourier(Functions.fourier_1,Functions.random_mat)
        if Functions.flag_2:
            re_image = Functions.re_fourier(Functions.random_mat,Functions.fourier_2)
        if Functions.flag_1 and Functions.flag_2:
            re_image = Functions.re_fourier(Functions.fourier_1,Functions.fourier_2)
        Functions.visulaize(np.abs(re_image),3)
        return render_template('main.html')
    else:
        return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)


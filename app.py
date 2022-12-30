from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import json
from flask import jsonify

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
@app.route("/" ,methods=['POST','GET'])
def image():
    if request.method == 'POST':
        img1=request.files.get('image1')
        img2=request.files.get('image2')
        if img1 != None:
            imgs_save = img1.filename + '.jpg'
            img1.save(imgs_save)
        if img2 != None:
            imgs_save2 = img2.filename + '.jpg'
            img2.save(imgs_save2)

        return render_template('main.html')
    else:
        return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)


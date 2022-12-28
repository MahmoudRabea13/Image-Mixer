from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import json
from flask import jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/get', methods=['GET', 'POST'])
def get(jsdata):
    print(jsdata)
    return 'success'
@app.route('/post', methods=['GET', 'POST'])
def post():
    print('hello')
    print(request.form['data'])
    return 'success'
if __name__ == '__main__':
    app.run()

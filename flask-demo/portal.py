#!/opt/local/bin/python3
# encoding: UTF-8

from flask import Flask, current_app, g, render_template, send_from_directory
import jinja2
import json, os, subprocess
from waitress import serve

template_dir = os.path.abspath('static/')
app = Flask(__name__, template_folder=template_dir)


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static/', path)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def zsPlan():
    product = "ZStack"
    version = 1
    vector = ["Alpha", "Beta", "Gamma", "Delta"]
    return render_template("index.html", version = version, product = product, vector = vector)

@app.route('/version', methods=['GET'])
def version():
    a=1
    b=2
    c=a+b
    return str(c)


if __name__ == '__main__':
    app.secret_key="zstack-srm"
    #app.run(host='0.0.0.0', port=7000, debug = True)
    serve(app, host='0.0.0.0', port=9998)

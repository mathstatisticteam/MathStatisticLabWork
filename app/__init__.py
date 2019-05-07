import sys

from bokeh.util.string import encode_utf8
from flask import render_template

import flask

sys.path.append("app")

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    html = render_template('index.html')
    return encode_utf8(html)
import mimetypes
import sys

import flask
from bokeh.util.string import encode_utf8
from flask import render_template

mimetypes.add_type('module', '.js')
mimetypes.add_type('text/javascript', '.js')

sys.path.append("app")

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    html = render_template('index.html')
    return encode_utf8(html)

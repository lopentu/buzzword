# -*-coding: utf-8 -*-
from os.path import abspath, dirname, join
import logging
import json

from flask import Flask, render_template
import coloredlogs
import requests

coloredlogs.install(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def hello_world():
    # input_text = request.args.get('input_text')
    buzzword = '喵星人'
    return render_template(
        'buzz.html',
        buzzword=buzzword,
        conc=json.loads(
            join(dirname(abspath(__file__)), 'sample.json')
        ),
        method='get'
    )


@app.route('/<word>')
def buzz_flex(word):
    url = 'http://localhost:12346/%s' % word
    jdata = requests.get(url).text
    dic = json.loads(jdata)
    return render_template(
        'buzz.html',
        buzzword=word,
        conc=dic['conclist'],
        freq_by_month=json.dumps(dic['freq_by_month']),
        method='get'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12346, debug=True)

# -*-coding: utf-8 -*-
from flask import Flask, render_template, request
import coloredlogs
import datetime
import requests
import logging
import sqlite3
import random
import json

coloredlogs.install(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/static')


def get_from_cache(word):
    db = sqlite3.connect('buzz.db')
    cursor = db.cursor()
    cursor.execute('''SELECT word, json_data FROM cache WHERE (word=?)''', (word, ))
    res = cursor.fetchone()
    db.close()
    jdata = None
    if res:
        jdata = res[1]
        logger.info('Get from cache: "%s"' % word)
    return jdata


def insert_cache(word, jdata):
    db = sqlite3.connect('buzz.db')
    cursor = db.cursor()
    cursor.execute('''INSERT OR IGNORE INTO cache VALUES (?, ?)''', (word, jdata))
    db.commit()
    db.close()
    logger.info('"%s" cached!' % word)


def cqp_consult(word, conclist_limit=1000):
    cache = get_from_cache(word)
    if cache:
        jdata = cache
    else:
        url = 'http://lopen.linguistics.ntu.edu.tw:12346/%s' % word
        jdata = requests.get(url).text
        if 'Time-out' not in jdata:
            insert_cache(word, jdata)
    dic = json.loads(jdata)
    conclist = dic['conclist'][:conclist_limit]
    freq_by_month = json.dumps(dic['freq_by_month'])
    return conclist, freq_by_month


@app.route('/rate/<word>/<score>')
def rate(word, score):
    db = sqlite3.connect('buzz.db')
    cursor = db.cursor()
    ip = request.remote_addr
    now = datetime.datetime.now()
    cursor.execute('''REPLACE INTO rating VALUES (?, ?, ?, ?)''', (now, ip, word, score))
    db.commit()
    logger.debug('{}, {}, {}'.format(ip, word, score))
    return 'OK'


@app.route('/cqp/<word>')
def cqp(word):
    conclist, freq_by_month = cqp_consult(word)
    return freq_by_month


@app.route('/')
def index():
    buzzword = request.args.get('find_buzzword')
    default_word = random.choice(['喵星人', '汪星人', '女神', '男神', '小屁孩', '屁孩', '魯蛇', '富奸', '溫拿'])
    if not buzzword:
        buzzword = default_word
    conclist, freq_by_month = cqp_consult(buzzword)

    db = sqlite3.connect('buzz.db')
    cursor = db.cursor()
    ip = request.remote_addr

    if buzzword != default_word:
        now = datetime.datetime.now()
        cursor.execute('''INSERT INTO history VALUES (?, ?, ?)''', (now, ip, buzzword))

    cursor.execute('''SELECT score FROM rating WHERE (ip=? and word=?)''', (ip, buzzword))
    res = cursor.fetchone()
    score = res[0] if res else None

    cursor.execute('''SELECT COUNT(*) FROM rating WHERE (word=?)''', (buzzword, ))
    res = cursor.fetchone()
    count = res[0] if res else 0

    db.commit()
    db.close()

    return render_template(
        'buzz.html',
        buzzword=buzzword,
        conc=conclist,
        freq_by_month=freq_by_month,
        score=score,
        count=count,
        method='get'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)

# Using uWSGI
# uwsgi --http 0.0.0.0:12345 --module buzz --callable app --processes 4 --threads 10

# Create table
# CREATE TABLE history (datetime DATETIME, ip CHAR(20), word CHAR);
# CREATE TABLE cache (word PRIMARY KEY, json_data CHAR);

# CREATE TABLE rating (datetime DATETIME, ip CHAR(20), word CHAR, score INTEGER, UNIQUE (ip, word));
# CREATE UNIQUE INDEX rating_index ON rating (ip, word);

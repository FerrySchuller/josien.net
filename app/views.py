from flask import render_template, jsonify
import os, sys
sys.path.append(os.getenv('lib_dir'))
from app.lib.josienlib import db
from pprint import pprint
from app.app import app

db = db()


# certbot certonly --manual
cert = os.getenv('LETS_ENCRYPT', False)
cert_key = cert.split('.')[0]
@app.route("/.well-known/acme-challenge/{}".format(cert_key))
def letsencrypt():
    return "{}".format(cert)


@app.route('/dev')
def dev():
    omi = db.omi_wallet.find_one({},{ "_id": 0 })
    return render_template('dev.html', omi=omi)


@app.route('/')
def index():
    omi = db.omi_wallet.find_one({},{ "_id": 0 })

    return render_template('index.html', omi=omi)


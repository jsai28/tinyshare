from flask import Flask, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import hashlib
import base64
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/tinyshare'
db = SQLAlchemy(app)
CORS(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    tinyshare_url = db.Column(db.String(50))
    password = db.Column(db.String(100), nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Link: {self.original_url}"
    
    def __init__(self, original_url, tinyshare_url, password=None, expiry_date=None):
        self.original_url = original_url
        self.tinyshare_url = tinyshare_url
        self.password = password
        self.expiry_date = expiry_date

def format_link(link):
    return {
        "id": link.id,
        "original_url": link.original_url,
        "tinyshare_url": link.tinyshare_url,
        "password": link.password,
        "expiry_date": link.expiry_date,
        "created_at": link.created_at,
    }

def create_tinyshare_url(original_url):
    hash_object = hashlib.sha256((original_url+str(time.time())).encode())
    hash_hex = hash_object.hexdigest()
    short_code = base64.urlsafe_b64encode(bytes.fromhex(hash_hex[:8])).decode()
    return short_code[:6]

@app.route('/')
def index():
    return 'Hello, World!'

# create a link
@app.route('/link', methods = ['POST'])
def create_link():
    original_url = request.json['original_url']
    password = request.json['password']
    expiry_date = request.json['expiry_date']
    tinyshare_url = create_tinyshare_url(original_url)
    link = Link(original_url, tinyshare_url, password, expiry_date)
    db.session.add(link)
    db.session.commit()
    return format_link(link)

# get all links
@app.route('/link', methods = ['GET'])
def get_links():
    links = Link.query.order_by(Link.id.asc()).all()
    links_list = []

    for link in links:
        links_list.append(format_link(link))
    
    return {'links': links_list}

# get single link
@app.route('/link/<id>', methods=['GET'])
def get_link(id):
    link = Link.query.filter_by(id=id).one()
    formatted_link = format_link(link)

    return {'link': formatted_link}

# delete a link
@app.route('/link/<id>', methods=['DELETE'])
def delete_link(id):
    link = Link.query.filter_by(id=id).one()
    db.session.delete(link)
    db.session.commit()
    return f'Link (id: {id}) deleted!'

# edit a link
@app.route('/link/<id>', methods=['PUT'])
def update_link(id):
    link = Link.query.filter_by(id=id)
    original_url = request.json['original_url']
    link.update(dict(original_url=original_url, created_at=datetime.now()))
    db.session.commit()
    return {'link': format_link(link.one())}

# reroute link
@app.route('/<short_code>')
def redirect_to_original(short_code):
    link = Link.query.filter_by(tinyshare_url=short_code).first()
    if link is None:
        abort(404)
    return redirect(link.original_url, code=301)

if __name__ == "__main__":
    app.run()
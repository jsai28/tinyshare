from flask import Flask, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/tinyshare'
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(250))
    original_url = db.Column(db.String(500))
    tinyshare_url = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Link: {self.title}"
    
    def __init__(self, title, description, original_url, tinyshare_url):
        self.title = title
        self.description = description
        self.original_url = original_url
        self.tinyshare_url = tinyshare_url

def format_link(link):
    return {
        "id": link.id,
        "title": link.title,
        "description": link.description,
        "original_url": link.original_url,
        "tinyshare_url": link.tinyshare_url,
        "created_at": link.created_at,
    }

def create_tinyshare_url(original_url):
    hash_object = hashlib.sha256(original_url.encode())
    hash_hex = hash_object.hexdigest()
    short_code = base64.urlsafe_b64encode(bytes.fromhex(hash_hex[:8])).decode()
    return short_code[:6]

@app.route('/')
def index():
    return 'Hello, World!'

# create a link
@app.route('/link', methods = ['POST'])
def create_link():
    title = request.json['title']
    description = request.json['description']
    original_url = request.json['original_url']
    tinyshare_url = create_tinyshare_url(original_url)
    link = Link(title, description, original_url, tinyshare_url)
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
    title = request.json['title']
    description = request.json['description']
    original_url = request.json['original_url']
    link.update(dict(title=title, description=description, original_url=original_url, created_at=datetime.now()))
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
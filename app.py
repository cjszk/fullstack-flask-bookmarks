from flask import Flask, render_template, request, session, g, json, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgres://rxvnpszm:Jk-I8WQEoEczmxmBsIuehJzhVENQArtd@elmer.db.elephantsql.com:5432/rxvnpszm',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

class bookmarks(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False, index=True)
    rating = db.Column(db.Integer)
    description = db.Column(db.String(500))

    def __init__ (self, title, url, rating, description):
        self.title = title
        self.url = url
        self.rating = rating
        self.description = description

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __repr__(self):
        data = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'rating': self.rating,
            'description': self.description
        }
        # return '[title: {}, url: {}, rating: {}, description: {}]'.format(self.title, self.url, self.rating, self.description)
        return str(data)
        

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/get', methods = ['GET'])
def api_get():
    data = []

    for item in bookmarks.query.all():
        data.append({
            'id': item.id,
            'title': item.title,
            'url': item.url,
            'rating': item.rating,
            'description': item.description
        })

    # js = json.dumps(data)

    # resp = Response(js, status = 200, mimetype='application/json')
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'https://web-bookmarker.herokuapp.com'
    return resp

@app.route('/post', methods = ['POST'])
def api_post():
    data = request.get_json()

    new_item = {
        'title': data['title'],
        'url': data['url'],
        'rating': data['rating'],
        'description': data['description']
    }

    post = bookmarks(new_item['title'], new_item['url'], new_item['rating'], new_item['description'])

    db.session.add(post)
    db.session.commit()


    return jsonify(data)

@app.route('/patch/<int:id>', methods =['PATCH'])
def api_patch(id):
    data = request.get_json()
    item = bookmarks.query.get(id)

    for key in data:
        if key == 'url':
            item.url = data['url']
        elif key == 'rating':
            item.rating = data['rating']
        elif key == 'description':
            item.description = data['description']
        elif key == 'title':
            item.title = data['title']

    db.session.commit()

    return jsonify(data)

@app.route('/delete/<int:id>', methods = ['DELETE'])
def api_delete(id):
    item = bookmarks.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return 'Deleted: {}'.format(id)

if __name__ == "__main__":
    db.create_all()
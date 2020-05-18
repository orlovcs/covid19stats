from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published
        }

class Infections(db.Model):
    __tablename__ = 'us_infections'

    id = db.Column(db.Integer, primary_key=True)
    combined_key = db.Column(db.String())
    date = db.Column(db.String())
    cases = db.Column(db.Integer())
    country_region = db.Column(db.String())
    province_state = db.Column(db.String())

    def __init__(self, index):
        self.id = id

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
        }
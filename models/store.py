from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    store = db.relationship('ItemModel',lazy ='dynamic')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name ,'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.delete(self)
        db.session.commit()

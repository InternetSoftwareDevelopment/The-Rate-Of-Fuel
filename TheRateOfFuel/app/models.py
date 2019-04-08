from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(client_id):
    return Client.query.get(int(client_id))

class Client(db.Model, UserMixin):
    clientID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    quotes = db.relationship('Quotes', backref='author', lazy=True)

    def get_id(self): return (self.clientID)

    def __repr__(self):
        return f"Client('{self.username}', '{self.name}', '{self.phone}', '{self.email}', '{self.address}'," \
               f" '{self.city}', '{self.state}', '{self.zip}')"

class Quotes(db.Model):
    quoteID = db.Column(db.Integer, primary_key=True)
    gallonsRequested = db.Column(db.Float, nullable=True)
    requestDate = db.Column(db.String(10), nullable=True)
    deliveryDate = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    suggestedPrice = db.Column(db.Float, nullable=True)
    totalAmountDue = db.Column(db.Float, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.clientID'), nullable=False)

    def __repr__(self):
        return f"Quotes('{self.gallonsRequested}', '{self.requestDate}', '{self.deliveryDate}', '{self.address}'," \
               f" '{self.city}', '{self.state}', '{self.zip}', '{self.name}', '{self.phone}', '{self.email}'," \
               f" '{self.suggestedPrice}','{self.totalAmountDue}')"
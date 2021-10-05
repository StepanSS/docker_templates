from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")
    print(app.config.get('SQLALCHEMY_DATABASE_URI'))

    db.init_app(app)

    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    @app.route("/get")
    def get_data():
        user = User.query.first()
        if user:
            print(user.email)
        return jsonify(hello="users")

    @app.route("/add")
    def add_data():
        db.session.add(User(email="michael@mherman.org"))
        db.session.commit()
        return jsonify(hello="users added")

    @app.route("/add_all")
    def add_all():
        person_1 = Person(name="John")
        person_2 = Person(name="Jim")
        person_3 = Person(name="Den")
        db.session.add(person_1)
        db.session.add(person_2)
        db.session.add(person_2)
        db.session.commit()
        return jsonify(hello="users added")



    return app


# One-to-Many Relationships
# ====================================================================================
class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True, cascade="all,delete")

    def __repr__(self):
        return f'id: {self.id}, email: {self.name}, address: {self.addresses}'

class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id',
                                                     onupdate='CASCADE',
                                                     ondelete='CASCADE'),
                        nullable=False)

    def __repr__(self):
        return f'id: {self.id}, email: {self.email}, person_id: {self.person_id}'


# One-to-Many Relationships
# ====================================================================================
association_table = db.Table('association_table',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id', ondelete="CASCADE")),
    db.Column('user_id', db.Integer, db.ForeignKey('users_demo.id', ondelete="CASCADE"))
)
class UserDemo(db.Model):
    __tablename__ = "users_demo"

    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(128), unique=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
        
    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(128), unique=True)
    users = db.relationship("UserDemo",
                               secondary=association_table)








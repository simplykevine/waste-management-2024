# Description: This file contains the models for the database tables. The User class inherits from db.Model and UserMixin. The WasteCollection class inherits from db.Model. The RecyclingEffort class inherits from db.Model. The User class has a one-to-many relationship with the WasteCollection class and the RecyclingEffort class. The WasteCollection class has a many-to-one relationship with the User class. The RecyclingEffort class has a many-to-one relationship with the User class. The User class has the following columns: id, email, username, password, date_created. The WasteCollection class has the following columns: id, user_id, address, collection_date, collection_time, status. The RecyclingEffort class has the following columns: id, user_id, date, materials, status. The __repr__ method is defined for the WasteCollection and RecyclingEffort classes to return a string representation of the object.
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a User class that inherits from db.Model and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    waste_collections = db.relationship('WasteCollection')
    recycling_efforts = db.relationship('RecyclingEffort')

# Create a WasteCollection class that inherits from db.Model
class WasteCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(256))
    collection_date = db.Column(db.Date)
    collection_time = db.Column(db.Time)
    status = db.Column(db.String(64))

    def __repr__(self):
        return f'<WasteCollection {self.collection_date}>' # Return a string representation of the WasteCollection object
    
# Create a RecyclingEffort class that inherits from db.Model
class RecyclingEffort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # This is the foreign key
    date = db.Column(db.DateTime, default=datetime.utcnow)
    materials = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    def __repr__(self):
         return f'<RecyclingEffort {self.date}>' # Return a string representation of the RecyclingEffort object
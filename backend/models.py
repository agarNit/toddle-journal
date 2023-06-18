from marshmallow import post_load
from backend.database import db
import datetime as dt
    
class Students(db.Model):
    __tablename__ = 'Students'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))
    
    @post_load
    def make_user(self, data, **kwargs):
        return Students(**data)
    
class Teachers(db.Model):
    __tablename__ = 'Teachers'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    teacher_username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))
    
    @post_load
    def make_user(self, data, **kwargs):
        return Teachers(**data)
    
class Journals(db.Model):
    __tablename__ = 'Journals'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(1000), nullable = False)
    attachment = db.Column(db.String(1000), nullable = False)
    published_at = db.Column(db.String(100), default = "", nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("Teachers.id"))
    student_tagged = db.Column(db.JSON, nullable = False)
    
    @post_load
    def make_user(self, data, **kwargs):
        return Journals(**data)
    
class Tagged(db.Model):
    __tablename__ = 'Tagged'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.Integer, db.ForeignKey("Students.id"))
    journal_id = db.Column(db.Integer, db.ForeignKey("Journals.id"))

    @post_load
    def make_user(self, data, **kwargs):
        return Tagged(**data)
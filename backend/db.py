import base64
from flask import jsonify, json
from backend.models import Students, Teachers, Journals, Tagged
from backend.database import db
import datetime as dt
import sqlite3
import os
import io
from flask_mail import Mail, Message
from flask import current_app as app

mail = Mail(app)

conn = sqlite3.connect('./db_directory/db.sqlite3', check_same_thread=False) 

class Database:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        pass

# -----------------------Student functions---------------------

    def all_students(self):
        cursor = conn.cursor() 
        cursor.execute("select * from Students")
        students = cursor.fetchall()
       
        output = []
        for student in students:
            output.append({
                'id': student[0],
                'student_username' : student[1],
                'email' : student[3]
            })
        return output

    def add_student(self, student):
        cursor = conn.cursor()
        cursor.execute("insert into Students (student_username, password, email) values (?, ?, ?)", (student['student_username'], student['password'], student['email']))
        conn.commit()
        return jsonify({'message': 'Student created successfully'})
    
    def get_student(self, id):
        cursor = conn.cursor()
        cursor.execute("select * from Students where id = ?", (id,))
        student = list(cursor.fetchone())
        if student is None:
            return jsonify({'message': 'Student not found'})
        output = []
        output.append({
            'id': student[0],
            'student_username' : student[1],
            'email' : student[3]
        })
        return output

    def get_student_by_username(self, username):
        cursor = conn.cursor()
        cursor.execute("select * from Students where student_username = ?", (username,))
        student = cursor.fetchone()

        if student is None:
            return student
        output = []
        output.append({
            'id': student[0],
            'student_username' : student[1],
            'email' : student[3]
        })
        return output
    
    def get_student_by_email(self, email):
        cursor = conn.cursor()
        cursor.execute("select * from Students where email = ?", (email,))
        student = cursor.fetchone()
        # print(student)
        if student is None:
            return student
        output = []
        output.append({
            'id': student[0],
            'student_username' : student[1],
            'email' : student[3]
        })
        return output
     
    def check_student_credentials(self, email, password):
        cursor = conn.cursor()
        cursor.execute("select * from Students where email = ? and password = ?", (email, password))
        student = cursor.fetchone()
        if student is None:
            return student
        output = []
        output.append({
            'id': student[0],
            'student_username' : student[1],
            'email' : student[3]
        })
        return output

# ----------------Teacher functions----------------
    
    def all_teachers(self):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers")
        teachers = cursor.fetchall()

        output = []
        for teacher in teachers:
            output.append({
                'id': teacher[0],
                'teacher_username' : teacher[1],
                'email' : teacher[3]
            })
        return output
    
    def add_teacher(self, teacher):
        cursor = conn.cursor()
        cursor.execute("insert into Teachers (teacher_username, password, email) values (?, ?, ?)", (teacher['teacher_username'], teacher['password'], teacher['email']))
        conn.commit()
        return jsonify({'message': 'Teacher created successfully'})
    
    def get_teacher(self, id):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers where id = ?", (id,))
        teacher = list(cursor.fetchone())
        if teacher is None:
            return jsonify({'message': 'Teacher not found'})
        output = []
        output.append({
            'id': teacher[0],
            'teacher_username' : teacher[1],
            'email' : teacher[3]
        })
        return output

    def get_teacher_by_username(self, username):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers where teacher_username = ?", (username,))
        teacher = cursor.fetchone()
        if teacher is None:
            return teacher
        output = []
        output.append({
            'id': teacher[0],
            'teacher_username' : teacher[1],
            'email' : teacher[3]
        })
        return output
    
    def get_teacher_by_email(self, email):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers where email = ?", (email,))
        teacher = cursor.fetchone()
        if teacher is None:
            return teacher
        output = []
        output.append({
            'id': teacher[0],
            'teacher_username' : teacher[1],
            'email' : teacher[3]
        })
        return output
     
    def check_teacher_credentials(self, email, password):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers where email = ? and password = ?", (email, password))
        teacher = cursor.fetchone()
        if teacher is None:
            return teacher
        output = []
        output.append({
            'id': teacher[0],
            'teacher_username' : teacher[1],
            'email' : teacher[3]
        })
        return output
    
# ----------------Journal functions----------------

    def all_journals(self):
        cursor = conn.cursor()
        cursor.execute("select * from Journals")
        journals = cursor.fetchall()

        output = []
        for journal in journals:
            output.append({
                'id': journal[0],
                'title' : journal[1],
                'description' : journal[2],
                'attachment': journal[3],
                'published_at' : journal[4],
                'teacher_id' : journal[5],
                'student_tagged': journal[6]
            })
        return output
    
    def get_journal(self, id):
        cursor = conn.cursor()
        cursor.execute("select * from Journals where id = ?", (id,))
        journal = list(cursor.fetchone())
        if journal is None:
            return jsonify({'message': 'Journals not found'})
        output = []
        output.append({
            'id': journal[0],
            'title' : journal[1],
            'description' : journal[2],
            'attachment': journal[3],
            'published_at' : journal[4],
            'teacher_id' : journal[5],
            'student_tagged': journal[6]
        })
        return output

    def get_journal_by_teacher(self, name):
        cursor = conn.cursor()
        cursor.execute("select * from Teachers where teacher_username = ?", (name,))
        teacher = cursor.fetchone()
        if teacher is None:
            return jsonify({'message': 'Teacher not found'})
        cursor.execute("select * from Journals where teacher_id = ?", (teacher[0],))
        journals = cursor.fetchall()
        if len(journals) == 0:
            return jsonify({'message': 'Journals not found'})
        
        output = []
        for journal in journals:
            output.append({
                'id': journal[0],
                'title' : journal[1],
                'description' : journal[2],
                'attachment': journal[3],
                'published_at' : journal[4],
                'teacher_id' : journal[5],
                'student_tagged': journal[6]
            })
        return output
    
    def get_journal_by_student(self, name):
        cursor = conn.cursor()
        cursor.execute("select * from Students where student_username = ?", (name,))
        student = cursor.fetchone()
        if student is None:
            return jsonify({'message': 'Student not found'})
        cursor.execute("select * from Tagged where student_id = ?", (student[0],))
        journal_ids = cursor.fetchall()
        if len(journal_ids) == 0:
            return jsonify({'message': 'Journals not found'})
        journals = []
        for journal_id in journal_ids:
            cursor.execute("select * from Journals where id = ?", (journal_id[1],))
            journal = cursor.fetchone()
            journals.append(journal)
        output = []
        for journal in journals:
            output.append({
                'id': journal[0],
                'title' : journal[1],
                'description' : journal[2],
                'attachment': journal[3],
                'published_at' : journal[4],
                'teacher_id' : journal[5],
                'student_tagged': journal[6]
            })
        return jsonify({'journals': output})
    
    def create_journal(self, data, id): 
        print(data['student_tagged'])
        student_list = data['student_tagged']
        for student in student_list:
            name = student_list[student]
            cursor = conn.cursor()
            cursor.execute("select * from Students where student_username = ?", (name,))
            student = cursor.fetchone()
            if student is None:
                return jsonify({'message': 'Some tagged students do not exist'})
        cursor = conn.cursor()

        cursor.execute("INSERT into Journals (title, description, attachment, teacher_id, student_tagged) values (?,?,?,?,?)",(data['title'], data['description'], data['attachment'], id, json.dumps(data['student_tagged'])))
        conn.commit()
        return "Journal successfully added."
    
    def update_journal(self, data, id):
        student_list = data['student_tagged']
        for student in student_list:
            name = student_list[student]
            cursor = conn.cursor()
            cursor.execute("select * from Students where student_username = ?", (name,))
            student = cursor.fetchone()
            if student is None:
                return jsonify({'message': 'Some tagged students do not exist'})
        cursor = conn.cursor()
        cursor.execute("select * from Journals where id = ?", (id,))
        journal = cursor.fetchone()
        if journal is None:
            return jsonify({'message': 'Journal not found'})
        cursor.execute("UPDATE Journals SET title = ?, description = ?, attachment = ?, student_tagged = ? WHERE id = ?",(data['title'],data['description'], data['attachment'] ,json.dumps(data['student_tagged']),id))
        conn.commit()
        return "Journal successfully updated."
    
    def delete_journal(self, id, teacher_id):
        cursor = conn.cursor()
        cursor.execute("select * from Journals where teacher_id = ? and id = ?", (teacher_id, id,))
        journal = cursor.fetchone()
        # print(journal, type(journal))
        # print(journal is None)
        if journal is None:
            return journal
        tagged_students = json.loads(journal[5])
        for student in tagged_students:
            name = tagged_students[student]
            # print(name)
            cursor.execute("select * from Students where student_username = ?", (name,))
            student = cursor.fetchone()
            cursor.execute("DELETE FROM Tagged WHERE student_id = ? and journal_id = ?",(student[0],id))
            conn.commit()

        cursor.execute("DELETE FROM Journals WHERE id = ?",(id,))
        conn.commit()
        return "Journal deleted successfully."
    
    def publish_journal(self, id):
        cursor = conn.cursor()
        cursor.execute("select * from Journals where id = ?", (id,))
        journal = cursor.fetchone()
        if journal is None:
            return jsonify({'message': 'Journal not found'})
        cursor.execute("UPDATE Journals SET published_at = ? WHERE id = ?",(dt.datetime.now(),id))
        # print(journal[5])
        students = json.loads(journal[5])
        for student in students:
            name = students[student]
            cursor.execute("select * from Students where student_username = ?", (name,))
            student = cursor.fetchone()
            if student is None:
                return jsonify({'message': 'Student not found'})
            cursor.execute("INSERT into Tagged (student_id, journal_id) values (?,?)",(student[0],id))
            msg = Message('Notification', sender ='flaskcard@gmail.com',recipients = [student[2]])
            msg.body = 'Dear {}, You have been tagged in a journal !!'.format(name)
            mail.send(msg)
            conn.commit()
        conn.commit()
        return "Journal published successfully."

    def get_journal_by_title(self, title):
        cursor = conn.cursor()
        cursor.execute("select * from Journals where title = ?", (title,))
        journal = cursor.fetchone()
        if journal is None:
            return journal
        output = []
        output.append({
            'id': journal[0],
            'title' : journal[1],
            'description' : journal[2],
            'attachment': journal[3],
            'published_at' : journal[4],
            'teacher_id' : journal[5],
            'student_tagged': journal[6]
        })
        return output

Db = Database()
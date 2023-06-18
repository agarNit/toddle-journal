from flask import jsonify, request
from backend.db import Db
from backend.models import Students, Teachers
from backend.errors import error_response
import jwt
from flask import current_app as app
from backend.database import db
from datetime import datetime, timedelta

@app.route('/student_signup', methods =['POST'])
def student_signup():
    student = request.json
    if student.get('student_username') == "" or student.get('confirm_password') == "" or student.get('email') == "" or student.get('password') == "":
        return error_response(400, "Fill all details.")
    
    duplicate_email = Db.get_student_by_email(student.get('email'))
    if duplicate_email != None:
        return error_response(400, "Student already exists.")
    
    user_exist = Db.get_student_by_username(student.get('student_username'))
    if user_exist != None:
        return error_response(400, "Username already taken.")
    
    if student.get('password') != student.get('confirm_password'):
        return error_response(400, "Passwords do not match.")
  
    if not user_exist:
        student = Db.add_student(student)
        return jsonify('Successfully registered.', 200)
    else:
        return jsonify('Email already registered. Use a different email.', 202)
                             
@app.route("/student_login", methods=["POST"])
def student_login():
    if not request.is_json:
        return error_response(400)

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response(400, "Email or password missing.")

    student = Db.check_student_credentials(email,password)
    if not student:
        return error_response(401, "Incorrect email or password.")
    
    token = jwt.encode({'student_username': student[0]['student_username'],'exp' : datetime.utcnow() + timedelta(minutes = 60)
            }, app.config['SECRET_KEY'])

    return jsonify({'token' : token }), 201


@app.route('/teacher_signup', methods =['POST'])
def teacher_signup():
    teacher = request.json
    if teacher.get('teacher_username') == "" or teacher.get('confirm_password') == "" or teacher.get('email') == "" or teacher.get('password') == "":
        return error_response(400, "Fill all details.")
    
    duplicate_name = Db.get_teacher_by_email(teacher.get('email'))
    if duplicate_name:
        return error_response(400, "Teacher already exists.")
    
    user_exist = Db.get_teacher_by_username(teacher.get('teacher_username'))
    if user_exist:
        return error_response(400, "Username already taken.")
    
    if teacher.get('password') != teacher.get('confirm_password'):
        return error_response(400, "Passwords do not match.")
  
    if not user_exist:
        teacher = Db.add_teacher(teacher)
        # add_teacher = Teachers(teacher_username = teacher.get('teacher_username'), email = teacher.get('email'), password = teacher.get('password'))
        return jsonify('Successfully registered.', 200)
    else:
        return jsonify('Email already registered. Use a different email.', 202)
                             
@app.route("/teacher_login", methods=["POST"])
def teacher_login():
    if not request.is_json:
        return error_response(400)

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response(400, "Email or password missing.")

    teacher = Db.check_teacher_credentials(email,password)
    if not teacher:
        return error_response(401, "Incorrect email or password.")
    
    token = jwt.encode({'teacher_username': teacher[0]['teacher_username'],'exp' : datetime.utcnow() + timedelta(minutes = 60)
            }, app.config['SECRET_KEY'])

    return jsonify({'token' : token }), 201

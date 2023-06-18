from flask import jsonify, request
from flask import current_app as app
from backend.db import Db
from backend.models import Teachers, Journals
from backend.errors import error_response
from functools import wraps
import jwt, os
from flask_mail import Message, Mail
from pathlib import Path

mail = Mail(app)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
			current_user = Db.get_teacher_by_username(data['teacher_username']) 
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
		return f(current_user, *args, **kwargs)
		# return redirect(url_for('dashboard', username = current_user.username))
	return decorated

@app.route("/teachers", methods=["GET"])
def all_teachers():
	students = Db.all_teachers()
	return jsonify(students)

@app.route("/curr_teacher", methods=["GET"])
@token_required
def teacher(current_user):
	# querying the database
	# for all the entries in it
	teacher = current_user
	# converting the query objects
	# to list of jsons
	return teacher

@app.route("/teacher/<string:name>", methods=["GET"])
@token_required
def get_teacher(current_user, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    return teacher

@app.route("/view_teacher_journals/<string:name>", methods=["GET"])
@token_required
def view_teacher_journals(current_user, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    journals = Db.get_journal_by_teacher(name)
    if journals is None:
        return jsonify("No journals available")
    return journals

@app.route("/add_journal/<string:name>", methods=["POST"])
@token_required
def add_journal(current_user, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    data = request.get_json()
    # print(attachment)
    # print(data)
    title = data['title']
    journal_exist = Db.get_journal_by_title(title)
    if journal_exist is not None:
         return "Journal already exists"
    journal = Db.create_journal(data, teacher[0].get('id'))
    return journal

@app.route("/update_journal/<int:id>/<string:name>", methods=["PUT"])
@token_required
def update_journal(current_user, id, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    data = request.get_json()
    journal = Db.update_journal(data, id)
    if journal is None: 
        return error_response(404, "Journal Not Found")
    return journal

@app.route("/delete_journal/<int:id>/<string:name>", methods=["DELETE"])
@token_required
def remove_journal(current_user, id, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    journal = Db.delete_journal(id, teacher[0].get('id'))
    if journal is None: 
        return error_response(404, "Journal not found for the particular teacher")
    return "Journal deleted"

@app.route("/publish_journal/<int:id>/<string:name>", methods=["POST"])
@token_required
def publish_journal(current_user, id, name):
    teacher = Db.get_teacher_by_username(current_user[0]['teacher_username'])
    if teacher is None:
        return error_response(404, "Teacher Not Found")
    if (teacher[0]['teacher_username'] != name):
        return error_response(401)
    journal = Db.publish_journal(id)
    if journal is None:
        return error_response(404, "Journal Not Found")
    return journal



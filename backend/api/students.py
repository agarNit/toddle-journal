from flask import jsonify, request
from flask import current_app as app
from backend.db import Db
from backend.models import Students
from backend.errors import error_response
from functools import wraps
import jwt

# conn = sqlite3.connect("./db_directory/db.sqlite3", check_same_thread=False)

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
			# current_user = Students.query.filter_by(student_username = data['student_username']).first()
			current_user = Db.get_student_by_username(data['student_username'])
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
		return f(current_user, *args, **kwargs)
		# return redirect(url_for('dashboard', username = current_user.username))
	return decorated


@app.route("/students", methods=["GET"])
def all_students():
	students = Db.all_students()
	# students = Db.all_students()
	return jsonify(students)

@app.route("/curr_student", methods=["GET"])
@token_required
def student(current_user):
	# querying the database
	# for all the entries in it
	student = current_user
	# converting the query objects
	# to list of jsons
	return student

@app.route("/student/<string:name>", methods=["GET"])
@token_required
def get_student(current_user, name):
    student = Db.get_student_by_username(current_user[0]['student_username'])
    if student is None:
        return error_response(404, "Student Not Found")
    if (student[0]['student_username'] != name):
        return error_response(401)
    return student

@app.route("/view_student_journals/<string:name>", methods=["GET"])
@token_required
def view_student_journals(current_user, name):
    student = Db.get_student_by_username(current_user[0]['student_username'])
    if student is None:
        return error_response(404, "Student Not Found")
    journals = Db.get_journal_by_student(name)
    if journals is None:
        return jsonify("No journals available")
    if (student[0]['student_username'] != name):
        return error_response(401)
    return journals


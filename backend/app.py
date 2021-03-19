from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_helpers
import route_helpers

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = "secret"
con = db_helpers.get_connection()

@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return jsonify({"message": "Missing file in request"}), 400
  status, msg = route_helpers.read_csv(request.files['file'], con)
  return jsonify({"message": msg}), status

@app.route('/report', methods=['GET'])
def get_report():
  status, report = route_helpers.generate_report(con)
  return jsonify(report), status

@app.route('/user', methods=['POST'])
def create_user():
  data = request.get_json()
  if 'password' not in data or 'username' not in data:
    return jsonify({"message": "username or password field missing"}), 400
  hashed_pwd = generate_password_hash(data['password'], method='sha256')
  status, msg = route_helpers.create_login(con, data['username'], hashed_pwd)
  return jsonify({"message": msg}), status

@app.route('/login', methods=['POST'])
def login():
  auth = request.get_json()
  if 'password' not in auth or 'username' not in auth:
    return jsonify({"message": "Please make sure both fields are entered"}), 401
  status, msg = route_helpers.check_login(con, auth['username'], auth['password'])
  return jsonify({"message": msg}), status


@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  return response

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_helpers
import route_helpers
import jwt
from functools import wraps

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = "secret"
con = db_helpers.get_connection()

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    if not token:
      return jsonify({"message": "Missing token in x-access-token header"}), 401

    try:
      jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
      return jsonify({"message": "Token is invalid"}), 401
    return f(*args, **kwargs)
  return decorated

@app.route('/upload', methods=['POST'])
@token_required
def upload_file():
  if 'file' not in request.files:
    return jsonify({"message": "Missing file in request"}), 400
  status, msg = route_helpers.read_csv(request.files['file'], con)
  return jsonify({"message": msg}), status

@app.route('/report', methods=['GET'])
@token_required
def get_report():
  status, report = route_helpers.generate_report(con)
  return jsonify(report), status

@app.route('/signup', methods=['POST'])
def create_user():
  data = request.get_json()
  if 'password' not in data or 'username' not in data:
    return jsonify({"message": "username or password field missing"}), 400
  hashed_pwd = generate_password_hash(data['password'], method='sha256')
  status, msg = route_helpers.create_login(con, data['username'], hashed_pwd)
  return jsonify({"message": msg}), status

@app.route('/login', methods=['POST'])
def login():
  auth = request.authorization
  if not auth or not auth.username or not auth.password:
    return jsonify({"message": "Please make sure both fields are entered"}), 401
  status, msg, id = route_helpers.check_login(con, auth.username, auth.password)
  if status == 200:
    token = jwt.encode({'user': id}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})
  return jsonify({"message": msg}), status


@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
  return response

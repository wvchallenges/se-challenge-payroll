from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash

from . import routes, con, token_required, jwtEncodedToDecoded, jwt, \
  route_helpers, SECRET_KEY


# create an admin user to use the application
@routes.route('/signup', methods=['POST'])
def create_user():
  data = request.get_json()
  if 'password' not in data or 'username' not in data:
    return jsonify({"message": "username or password field missing"}), 400
  hashed_pwd = generate_password_hash(data['password'], method='sha256')
  status, msg = route_helpers.create_user(con, data['username'], hashed_pwd)
  return jsonify({"message": msg}), status


# login as user, and return cookies with jwt token
@routes.route('/login', methods=['POST'])
def login():
  auth = request.authorization
  if not auth or not auth.username or not auth.password:
    return jsonify({"message": "Please make sure both fields are entered"}), 401
  status, msg, id = route_helpers.check_login(con, auth.username, auth.password)
  if status == 200:
    token = jwt.encode({'user': id}, SECRET_KEY, algorithm="HS256")
    jwtEncodedToDecoded[token] = id
    resp = make_response(jsonify({'token': token}), 200)
    resp.set_cookie('token', token, httponly=True, max_age=60*30)
    return resp
  return jsonify({"message": msg}), status


# verify jwt token is valid (used in frontend to make sure we are still logged in)
@routes.route('/verify', methods=['GET'])
def verify():
  token = None
  if 'token' in request.cookies:
    token = request.cookies['token']
  if not token:
    return jsonify({"message": "Unauthorized. Missing token in cookies"}), 401
  try:
    if token in jwtEncodedToDecoded:
      return jsonify({"message": "Success"}), 200
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    jwtEncodedToDecoded[token] = decoded
    return jsonify({"message": "Success"}), 200
  except:
    return jsonify({"message": "Token is invalid"}), 401


# logout the user and delete the jwt token cookie
@routes.route('/logout', methods=['POST'])
@token_required
def logout():
  resp = make_response(jsonify({}), 200)
  resp.delete_cookie('token')
  print("deleted cookie")
  return resp

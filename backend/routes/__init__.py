from flask import Blueprint
from db import db_helpers
import jwt
from functools import wraps
import os

routes = Blueprint('routes', __name__)

# used to encode jwt token
SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "http://localhost:3000"

CLIENT_URL = os.environ.get('CLIENT_URL') or "http://localhost:3000"

# get the initial connection from the db which will be used across all methods
con = db_helpers.get_connection()

# store a map of encoded jwt keys and their originals, for faster lookup
jwtEncodedToDecoded = {}

# generate report
@routes.route('/', methods=['GET'])
def hello():
  return "<h1>Flask app is running...</h1>"

# makes sure jwt token is present for certain request types
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'token' in request.cookies:
      token = request.cookies['token']
    if not token:
      return jsonify({"message": "Unauthorized. Missing token in cookies"}), 401

    try:
      if token in jwtEncodedToDecoded:
        pass
      else:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        jwtEncodedToDecoded[token] = decoded
    except:
      return jsonify({"message": "Token is invalid"}), 401
    return f(*args, **kwargs)

  return decorated


# cors and cookies headers required
@routes.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = CLIENT_URL
  header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
  header['Access-Control-Allow-Credentials'] = 'true'
  return response


from .admin import *
from .auth import *

print(CLIENT_URL)

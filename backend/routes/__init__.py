from flask import Blueprint
from db import db_helpers
import jwt
from functools import wraps

routes = Blueprint('routes', __name__)
SECRET_KEY = "secret"

con = db_helpers.get_connection()

jwtEncodedToDecoded = {}

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

from .admin import *
from .auth import *


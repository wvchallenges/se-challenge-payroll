from flask import Flask
from routes import *


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
# app.config["SECRET_KEY"] = "secret"
app.register_blueprint(routes)

@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
  header['Access-Control-Allow-Credentials'] = 'true'
  return response

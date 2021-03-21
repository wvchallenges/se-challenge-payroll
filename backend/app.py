from flask import Flask
from routes import *


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(routes)

# @app.after_request
# def after_request(response):
#   header = response.headers
#   header['Access-Control-Allow-Origin'] = '*' # http://localhost:3000
#   header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
#   header['Access-Control-Allow-Credentials'] = 'true'
#   return response

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

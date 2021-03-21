from flask import Flask
from routes import *


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(routes)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

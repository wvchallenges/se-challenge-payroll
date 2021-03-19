from flask import Flask, request, jsonify

from db import db_helpers
import route_helpers

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
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

@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  return response

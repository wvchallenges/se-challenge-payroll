from flask import request, jsonify

from . import routes, con, token_required, route_helpers

# upload csv
@routes.route('/upload', methods=['POST'])
@token_required
def upload_file():
  if 'file' not in request.files:
    return jsonify({"message": "Missing file in request"}), 400
  status, msg = route_helpers.read_csv(request.files['file'], con)
  return jsonify({"message": msg}), status

# generate report
@routes.route('/report', methods=['GET'])
@token_required
def get_report():
  status, report = route_helpers.generate_report(con)
  return jsonify(report), status

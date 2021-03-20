from flask import request, jsonify

from . import routes, con, token_required, route_helpers


@routes.route('/upload', methods=['POST'])
@token_required
def upload_file():
  if 'file' not in request.files:
    return jsonify({"message": "Missing file in request"}), 400
  status, msg = route_helpers.read_csv(request.files['file'], con)
  return jsonify({"message": msg}), status

@routes.route('/report', methods=['GET'])
@token_required
def get_report():
  status, report = route_helpers.generate_report(con)
  return jsonify(report), status

# @routes.after_request
# def after_request(response):
#   header = response.headers
#   header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
#   header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
#   header['Access-Control-Allow-Credentials'] = 'true'
#   return response

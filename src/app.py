from flask import Flask
from flask_restful import Api

from src.api.payroll_api import PayrollApi

app = Flask(__name__)
api = Api(app)

api.add_resource(PayrollApi, "/payroll")

app.run(host='0.0.0.0', port=8080, debug=False)

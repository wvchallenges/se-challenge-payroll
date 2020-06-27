import inject
from flask import Flask
from flask_restful import Api


def my_config(binder):
    pass


inject.configure(my_config)

from src.api.payroll_api import PayrollApi

app = Flask(__name__)
api = Api(app)

api.add_resource(PayrollApi, "/payroll")


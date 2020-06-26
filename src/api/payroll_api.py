import inject
from flask_restful import Resource

from src.service.payroll_service import PayrollService


class PayrollApi(Resource):
    payroll_service = inject.instance(PayrollService)

    def get(self):
        pass

    def post(self):
        pass

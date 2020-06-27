import inject
from flask import jsonify
from flask_restful import Resource

from src.service.payroll_service import PayrollService


class PayrollApi(Resource):
    payroll_service = inject.instance(PayrollService)

    def get(self):
        report = self.payroll_service.get_report()
        return jsonify(payrollReport=report)

    def post(self):
        pass

import inject
from flask import jsonify
from flask_restful import Resource

from src.service.payroll_service import PayrollService


class PayrollApi(Resource):
    payroll_service = inject.instance(PayrollService)

    def get(self):
        full_report = {"employeeReports": self.payroll_service.get_employee_report()}
        return jsonify(payrollReport=full_report)

    def post(self):
        pass

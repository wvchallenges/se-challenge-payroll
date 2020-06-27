import unittest
from unittest.mock import patch

from flask import Flask

from src.api.payroll_api import PayrollApi
from src.service.payroll_service import PayrollService


class TestPayrollApi(unittest.TestCase):
    payroll_api = PayrollApi()

    def setUp(self) -> None:
        self.app = Flask(__name__)

    @patch.object(PayrollService, 'get_employee_report')
    def test_return_empty_when_no_info(self, mock_get_report):
        mock_get_report.return_value = []

        with self.app.app_context():
            result = self.payroll_api.get()
            self.assertIsNotNone(result)
            self.assertEqual(result.status_code, 200)
            self.assertTrue(result.json)
            self.assertTrue("payrollReport" in result.json)
            self.assertTrue(len(result.json["payrollReport"]) == 1, result.json["payrollReport"])
            self.assertTrue("employeeReports" in result.json["payrollReport"])
            self.assertTrue(len(result.json["payrollReport"]["employeeReports"]) == 0, result.json["payrollReport"])

    @patch.object(PayrollService, 'get_employee_report')
    def test_return_emp_1_info_when_info_is_present(self, mock_get_report):
        mock_return = {
            "employeeId": 1,
            "payPeriod": {
                "startDate": "2020-01-01",
                "endDate": "2020-01-15"
            },
            "amountPaid": "$300.00"
        }
        mock_get_report.return_value = [mock_return]

        with self.app.app_context():
            result = self.payroll_api.get()

            self.assertIsNotNone(result)
            self.assertEqual(result.status_code, 200)
            self.assertTrue(result.json)
            self.assertTrue("payrollReport" in result.json)
            self.assertTrue(len(result.json["payrollReport"]) == 1, result.json["payrollReport"])
            self.assertTrue("employeeReports" in result.json["payrollReport"])
            self.assertTrue(len(result.json["payrollReport"]["employeeReports"]) == 1, result.json["payrollReport"])
            self.assertEqual(result.json["payrollReport"]["employeeReports"][0], mock_return)

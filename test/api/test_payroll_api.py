from unittest.mock import patch

import pytest

from src import app
from src.service.payroll_service import PayrollService


@pytest.fixture(scope="function")
def client():
    with app.test_client() as client:
        yield client


@patch.object(PayrollService, 'get_employee_report')
def test_return_empty_when_no_info(mock_get_employee_report, client):
    mock_get_employee_report.return_value = []

    result = client.get("/payroll")
    assert result is not None
    assert result.status_code == 200, result.status_code
    assert result.json
    assert "payrollReport" in result.json
    assert len(result.json["payrollReport"]) == 1, result.json["payrollReport"]
    assert "employeeReports" in result.json["payrollReport"]
    assert len(result.json["payrollReport"]["employeeReports"]) == 0, result.json["payrollReport"]


@patch.object(PayrollService, 'get_employee_report')
def test_return_emp_1_info_when_info_is_present(mock_get_report, client):
    mock_return = {
        "employeeId": 1,
        "payPeriod": {
            "startDate": "2020-01-01",
            "endDate": "2020-01-15"
        },
        "amountPaid": "$300.00"
    }
    mock_get_report.return_value = [mock_return]

    result = client.get("/payroll")

    assert result is not None
    assert result.status_code == 200, result.status_code
    assert result.json
    assert "payrollReport" in result.json
    assert len(result.json["payrollReport"]) == 1, result.json["payrollReport"]
    assert "employeeReports" in result.json["payrollReport"]
    assert len(result.json["payrollReport"]["employeeReports"]) == 1, result.json["payrollReport"]
    assert result.json["payrollReport"]["employeeReports"][0] == mock_return


def test_fail_payroll_report_upload_when_file_name_is_wrong(client):
    upload_data = {"invalid_file_name.csv": ""}
    result = client.post("/payroll", data=upload_data)
    assert result is not None
    assert result.status_code == 400, result.data

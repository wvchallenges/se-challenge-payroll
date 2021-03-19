import datetime
import json
import os
import re
from collections import OrderedDict

from flask import Flask, request, jsonify

import db

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
con = db.get_connection('example.db')

@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return jsonify({"message": "Missing file in request"}), 400
  status, msg = read_csv(request.files['file'], con)
  return jsonify({"message": msg}), status

@app.route('/report', methods=['GET'])
def get_report():
  status, report = generate_report(con)
  return jsonify(report), status

def main():
  con = db.initialize_db('example.db')
  # read_csv('time-report-42.csv', con)
  # generate_report(con)

def read_csv(file_handler, con):

  filename = file_handler.filename
  report_num = re.findall(r"time-report-(\d+)\.csv",filename)[0]

  if db.exists_report(con, report_num):
    return 409, f"Report num {report_num} exists. Not doing anything"

  line_count = 0
  for row in file_handler.readlines():
    date, hours, employee, job = row.decode("utf-8").strip().split(",")
    if line_count == 0:
      print(f'Column names are {row}')
    else:
      try:
        db.insert_csv_row(con, date, hours, employee, job, report_num)
      except Exception as e:
        return 500, e.args[0]

    line_count += 1
  return 200, "File uploaded successfully"

def generate_report(con):
  try:
    rows = db.get_records_sorted(con)
  except Exception as e:
    return 500, e.args[0]

  employeeReports = OrderedDict()

  for emp_id, timestamp, earnings in rows:
    report = OrderedDict()
    report["employeeId"] = int(emp_id)
    amountPaid = f"${earnings}"
    payPeriod = calculatePeriod(timestamp, emp_id, employeeReports)

    # see if we can merge this with another entry
    key = f"{emp_id}-{payPeriod['endDate']}"
    if key in employeeReports:
      # update the earnings
      currentEarnings = float(employeeReports[key]["amountPaid"][1:])
      employeeReports[key]["amountPaid"] = f"${currentEarnings + float(earnings)}"
    else:
      report["payPeriod"] = payPeriod
      report["amountPaid"] = amountPaid
      print(report)
      employeeReports[key] = report

  employeeReportsList = [employeeReports[key] for key in employeeReports]
  res = OrderedDict()
  res["payrollReport"] = {}
  res["payrollReport"]["employeeReports"] = employeeReportsList
  json_res = json.dumps(res)

  return 200, res

def calculatePeriod(timestamp, emp_id, employeeReports):
  NUM_DAYS_PER_MONTH = {1:31, 2:28, 3:31, 4:3, 5:31, 6:30,
                        7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
  dt = datetime.datetime.fromtimestamp(timestamp)
  month, day, year = dt.month, dt.day, dt.year
  dates = OrderedDict()
  num_days = NUM_DAYS_PER_MONTH[dt.month]
  mid_day = 15
  if dt.day <= mid_day:
    # pay is for first half
    startDate = f"{year}-{month}-01"
    endDate = f"{year}-{month}-{mid_day}"
  else:
    # pay is for last half
    startDate = f"{year}-{month}-{mid_day + 1}"
    endDate = f"{year}-{month}-{num_days}"
    # maybe we alawys set to 16 days?
    # if f"{emp_id}-{startDate}" in employeeReports:
    #   startDate = f"{year}-{month}-{mid_day + 1}"

  dates["startDate"] = startDate
  dates["endDate"] = endDate
  return dates

if __name__ == "__main__":
  os.remove('example.db')
  # main()
  pass

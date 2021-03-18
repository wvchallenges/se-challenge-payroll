import re

import db
import csv
import os
from collections import OrderedDict
import datetime
import json

def main():
  con = db.initialize_db('example.db')
  read_csv('time-report-42.csv', con)
  generate_report(con)

def read_csv(csv_file, con):
  report_num = re.findall(r"time-report-(\d+)\.csv",csv_file)[0]
  with open(csv_file) as f:
    line_count = 0
    for row in f:
      date, hours, employee, job = row.strip().split(",")
      if line_count == 0:
        print(f'Column names are {row}')
      else:
        db.insert_csv_row(con, date, hours, employee, job, report_num)
      line_count += 1

def generate_report(con):
  rows = db.get_records_sorted(con)
  employeeReports = OrderedDict()

  for emp_id, timestamp, earnings in rows:
    report = OrderedDict()
    report["amountPaid"] = f"${earnings}"
    report["employeeId"] = int(emp_id)
    payPeriod = calculatePeriod(timestamp, emp_id, employeeReports)

    # see if we can merge this with another entry
    key = f"{emp_id}-{payPeriod['endDate']}"
    if key in employeeReports:
      # update the earnings
      currentEarnings = float(employeeReports[key]["amountPaid"][1:])
      employeeReports[key]["amountPaid"] = f"${currentEarnings + float(earnings)}"
    else:
      report["payPeriod"] = payPeriod
      employeeReports[key] = report

  employeeReportsList = [employeeReports[key] for key in employeeReports]
  res = OrderedDict()
  res["payrollReport"] = {}
  res["payrollReport"]["employeeReports"] = employeeReportsList
  json_res = json.dumps(res)
  print(json_res)

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
    endDate = f"{year}-{month}-{mid_day}"
    startDate = f"{year}-{month}-01"
  else:
    # pay is for last half
    endDate = f"{year}-{month}-{num_days}"
    startDate = f"{year}-{month}-{mid_day}"
    if f"{emp_id}-{startDate}" in employeeReports:
      startDate = f"{year}-{month}-{mid_day + 1}"

  # dates["date"] = f"{year}-{month}-{day}"
  dates["endDate"] = endDate
  dates["startDate"] = startDate
  return dates

if __name__ == "__main__":
  os.remove('example.db')
  main()

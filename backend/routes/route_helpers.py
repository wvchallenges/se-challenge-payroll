import re
from collections import OrderedDict
from datetime import datetime

from db import db_crud

NUM_DAYS_PER_MONTH = {1: 31, 2: 28, 3: 31, 4: 3, 5: 31, 6: 30,
                      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def read_csv(file_handler, con):
  # read csv passed in and insert into db
  # make sure csv has proper naming convention
  filename = file_handler.filename
  report_num = re.findall(r"time-report-(\d+)\.csv", filename)

  if not report_num:
    return 500, f"Either {filename} is not a csv, or it does not follow naming convention"

  # if report already exists, we return
  report_num = report_num[0]
  if db_crud.select_report(con, report_num):
    return 409, f"Report num {report_num} exists. Cannot reuse."

  # try to insert all rows, if no errors on any rows, proceed else return
  try:
    db_crud.insert_csv_rows(con, file_handler, report_num)
    return 200, f"File {filename} uploaded successfully"
  except Exception as e:
    return 500, e.args[0]


def generate_report(con):
  # get all records of employee logs, sorted by id and then by time
  try:
    rows = db_crud.select_records_sorted(con)
  except Exception as e:
    return 500, e.args[0]

  # we need ordered dict so we maintain the order we inserted
  employeeReports = OrderedDict()

  for emp_id, timestamp, earnings in rows:
    # inner json, consisting of id, pay period and amount paid
    report = OrderedDict()
    report["employeeId"] = str(emp_id)
    amountPaid = f"${earnings}"
    payPeriod = calculatePeriod(timestamp)

    # see if we can merge this with another entry, meaning if employee got paid
    # more than once in the same pay period
    key = f"{emp_id}-{payPeriod['endDate']}"
    if key in employeeReports:
      # there's already a record, so update the earnings in that record
      currentEarnings = float(employeeReports[key]["amountPaid"][1:])
      employeeReports[key][
        "amountPaid"] = "${:.2f}".format(currentEarnings + float(earnings))
    else:
      # no record, add it in
      report["payPeriod"] = payPeriod
      report["amountPaid"] = "${:.2f}".format(float(earnings))
      employeeReports[key] = report

  # finalize json
  employeeReportsList = [employeeReports[key] for key in employeeReports]
  res = OrderedDict()
  res["payrollReport"] = {}
  res["payrollReport"]["employeeReports"] = employeeReportsList

  return 200, res


def calculatePeriod(timestamp):
  # convert unix timestamp to human date
  dt = datetime.fromtimestamp(timestamp)
  month, day, year = dt.month, dt.day, dt.year
  if len(str(month)) == 1:
    month = f"0{month}"

  # dates is our pay period object
  dates = OrderedDict()
  num_days = NUM_DAYS_PER_MONTH[dt.month]
  mid_day = 15

  # see which category this employee falls in
  if dt.day <= mid_day:
    # pay is for first half
    startDate = f"{year}-{month}-01"
    endDate = f"{year}-{month}-{mid_day}"
  else:
    # pay is for last half
    startDate = f"{year}-{month}-{mid_day + 1}"
    endDate = f"{year}-{month}-{num_days}"

  dates["startDate"] = startDate
  dates["endDate"] = endDate
  return dates


def create_user(con, username, password):
  # create the user when initially signing up, error if exists
  try:
    db_crud.create_user(con, username, password)
    return 200, f"Successfully created user {username}"
  except Exception as e:
    return 500, e.args[0]


def check_login(con, username, password):
  # verify username and password when logging in
  try:
    id = db_crud.select_check_user(con, username, password)
    if not id:
      return 401, "User does not exist or password is incorrect", -1
    return 200, f"Successfully logged in for user {username}", id
  except Exception as e:
    return 500, e.args[0], -1

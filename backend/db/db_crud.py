from datetime import datetime

from db import db_helpers
import time
from werkzeug.security import check_password_hash
import uuid

########### INSERT ###########

def insert_csv_rows(con, file_handler, report_num):
  # read through each csv file row, and see if we can insert
  cur = con.cursor()

  line_count = 0
  for row in file_handler.readlines():
    if line_count == 0:
      print(f'Headers are {row.strip()}')
    else:
      try:
        # assumed to be valid, but check for error regardless
        date, hours, employee, job = row.decode("utf-8").strip().split(",")
        insert_csv_row(cur, date, hours, employee, job, report_num)
      except Exception as e:
        # there was an error on a certain row, we cannot continue, roll back
        db_helpers.exception_handler(con, e, f"Error on line {line_count + 1}. Not uploading file")
    line_count += 1

  try:
    # everything was good, so commit
    con.commit()
    print('Inserted row')
    cur.close()
  except Exception as e:
    db_helpers.exception_handler(con, e, f"Unable to commit changes")

def insert_csv_row(cur, date, hours, emp_id, job, report_num):
  # insert a single row into the databse
  # make sure employee exists in the EMPLOYEE table, if not, insert
  cur.execute('''INSERT OR REPLACE INTO EMPLOYEES (id) VALUES (?)''', (emp_id,))

  # make sure job exists in the JOB table, it should because we pre populate
  if not select_job_check(cur, job):
    raise Exception(f"Job {job} does not exist in JOB table")

  # convert dd/mm/yyyy into datetime
  try:
    log_date = time.mktime(
      datetime.strptime(date.replace("/0", "/"), '%d/%m/%Y').timetuple())
  except Exception as e:
    raise Exception(f"Unable to convert date {date} to datetime: {e}")

  # insert into EMPLOYEE_LOG
  try:
    cur.execute(
      '''INSERT INTO EMPLOYEE_LOGS (employee_id, log_date, hours, job_name, report_num) VALUES (?,?,?,?,?)''',
      (emp_id, log_date, hours, job, report_num))
    print('Inserted row')
  except Exception as e:
    raise Exception(f"Skipping row: {e}")

########### SELECT ###########
def select_job_check(cur, job):
  # see if job exists, if not, we cannot insert this csv file
  cur.execute('''SELECT * FROM JOBS WHERE name=?''', (job,))

  rows = cur.fetchall()
  if not rows:
    return False

  return True

def select_records_sorted(con):
  # get our report records, sorted by employee id and then time
  cur = con.cursor()
  try:
    cur.execute(
      '''SELECT employee_id as employeeId, log_date, (hours * rate) AS 
      amountPaid FROM EMPLOYEE_LOGS INNER JOIN JOBS WHERE 
      EMPLOYEE_LOGS.job_name = JOBS.name ORDER BY employee_id ASC, log_date ASC''')
    rows = cur.fetchall()
    cur.close()
    return rows
  except Exception as e:
    db_helpers.exception_handler(con, e,
                                 "Cannot continue since report generation failed on db")


def select_report(con, report_num):
  # see if report num exists, if it does, we cannot insert this csv
  # report num is checked through the EMPLOYEE_LOGS table
  cur = con.cursor()
  try:
    cur.execute(
      '''SELECT report_num FROM EMPLOYEE_LOGS WHERE report_num=? LIMIT 1''',
      (report_num,))
    rows = cur.fetchall()
    cur.close()

    # if no result, it does not exist, else it does
    if not rows:
      return False
    return True
  except Exception as e:
    db_helpers.exception_handler(con, e,
                                 "Cannot continue since checking if report num exists failed on db")

def select_check_user(con, username, password):
  # see if username and password matches an entry
  # password is hashed
  cur = con.cursor()
  try:
    cur.execute('''SELECT id, password FROM ADMINS WHERE username=?''', (username,))
    rows = cur.fetchall()
    cur.close()

    # if not rows, this means username does not exist in table
    if not rows:
      return False
    # username exists, make sure password matches
    if not check_password_hash(rows[0][1], password):
      return False
    # return the user id
    return rows[0][0]
  except Exception as e:
    db_helpers.exception_handler(con, e, f"Unable to check for user in database")

########### CREATE ###########
def create_user(con, username, password):
  # create a login user which will be used to perform actions
  cur = con.cursor()
  try:
    # associate an uuid with it since this is what the jwt token will be based
    # off of, it is much harder to forge
    id = str(uuid.uuid4())
    cur.execute('''INSERT INTO ADMINS (id, username, password) VALUES (?,?,?)''', (id, username, password))
    con.commit()
    print('Inserted user')
    cur.close()
    return con
  except Exception as e:
    db_helpers.exception_handler(con, None, f"Unable to create user {username}. Most likely already exists")

from datetime import datetime

from db import db_helpers
import time


def insert_employee_check(con, emp_id):
  cur = con.cursor()
  cur.execute('''INSERT OR REPLACE INTO EMPLOYEES (id) VALUES (?)''', (emp_id,))
  cur.close()


def insert_job_check(con, job):
  cur = con.cursor()
  cur.execute('''SELECT * FROM JOBS WHERE name=?''', (job,))

  rows = cur.fetchall()
  cur.close()
  if not rows:
    return False

  return True


def insert_csv_row(con, date, hours, emp_id, job, report_num):
  # make sure employee exists in the EMPLOYEE table, if not, insert
  insert_employee_check(con, emp_id)

  # make sure job exists in the JOB table, it should because we pre populate
  if not insert_job_check(con, job):
    db_helpers.exception_handler(con, None,
                                 f"Will not insert row because job {job} does not exist in JOB table")

  # convert dd/mm/yyyy into datetime
  try:
    log_date = time.mktime(
      datetime.strptime(date.replace("/0", "/"), '%d/%m/%Y').timetuple())
  except Exception as e:
    return db_helpers.exception_handler(con, None,
                                        f"Unable to convert date {date} to datetime: {e}")

  # insert into EMPLOYEE_LOG
  cur = con.cursor()
  try:
    cur.execute(
      '''INSERT INTO EMPLOYEE_LOGS (employee_id, log_date, hours, job_name, report_num) VALUES (?,?,?,?,?)''',
      (emp_id, log_date, hours, job, report_num))
    con.commit()
    print('Inserted row')
    cur.close()
    return con
  except Exception as e:
    db_helpers.exception_handler(con, e, "Skipping row")


def get_records_sorted(con):
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


def exists_report(con, report_num):
  cur = con.cursor()
  try:
    cur.execute(
      '''SELECT report_num FROM EMPLOYEE_LOGS WHERE report_num=? LIMIT 1''',
      (report_num,))
    rows = cur.fetchall()
    cur.close()
    if not rows:
      return False
    return True  # should be true
  except Exception as e:
    db_helpers.exception_handler(con, e,
                                 "Cannot continue since checking if report num exists failed on db")

def create_user(con, username, password):
  cur = con.cursor()
  try:
    cur.execute('''INSERT INTO ADMINS (username, password) VALUES (?,?)''', (username, password))
    con.commit()
    print('Inserted user')
    cur.close()
    return con
  except Exception as e:
    db_helpers.exception_handler(con, e, f"Unable to create user {username}")

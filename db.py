import sqlite3 as sql
import datetime
import time
import sys

def exception_handler(con, e, msg):
  if con:
    con.rollback()

  if e:
    raise Exception(f"Unexpected error. {msg}: {e.args[0]}")
  raise Exception(f"Unexpected error. {msg}")

def get_connection(filename):
  con = None

  try:
    con = sql.connect(filename, check_same_thread=False)
    return con
  except Exception as e:
    exception_handler(con, e, "Cannot continue since db connect failed")
    exit(1)

def initialize_db(filename):
  con = None

  try:
    con = get_connection(filename)
    cur = con.cursor()

    # drop tables
    cur.execute('''DROP TABLE IF EXISTS EMPLOYEES''')
    cur.execute('''DROP TABLE IF EXISTS JOBS''')
    cur.execute('''DROP TABLE IF EXISTS EMPLOYEE_LOGS''')

    # create tables
    cur.execute('''CREATE TABLE EMPLOYEES (
    id INTEGER PRIMARY KEY
    )''')

    cur.execute('''CREATE TABLE JOBS (
    name TEXT PRIMARY KEY,
    rate INTEGER NOT NULL
    )''')

    cur.execute('''CREATE TABLE EMPLOYEE_LOGS (
    employee_id INTEGER NOT NULL,
    log_date DATE NOT NULL,
    hours REAL NOT NULL,
    job_name TEXT NOT NULL,
    report_num TEXT NOT NULL,
    FOREIGN KEY (employee_id)
      REFERENCES EMPLOYEE(id),
    FOREIGN KEY (job_name)
      REFERENCES JOB(name)
    )''')

    con.commit()
    cur.close()
    print("Database tables set up!")
    return con
  except Exception as e:
    exception_handler(con, e, "Cannot continue since db init failed")
    exit(1)

def migrate_db(filename):
  con = None

  try:
    con = get_connection(filename)
    cur = con.cursor()

    cur.execute('''DELETE FROM JOBS''')
    cur.execute('''INSERT INTO JOBS (name, rate) VALUES (?,?)''', ('A', 20,))
    cur.execute('''INSERT INTO JOBS (name, rate) VALUES (?,?)''', ('B', 30,))

    con.commit()
    cur.close()
    print("Database rows migrated!")
    return con
  except Exception as e:
    exception_handler(con, e, "Cannot continue since db migration failed")
    exit(1)

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
    exception_handler(con, None, f"Will not insert row because job {job} does not exist in JOB table")

  # convert dd/mm/yyyy into datetime
  try:
    log_date = time.mktime(datetime.datetime.strptime(date.replace("/0", "/"), '%d/%m/%Y').timetuple())
  except Exception as e:
    return exception_handler(con, None, f"Unable to convert date {date} to datetime: {e}")

  # insert into EMPLOYEE_LOG
  cur = con.cursor()
  try:
    cur.execute('''INSERT INTO EMPLOYEE_LOGS (employee_id, log_date, hours, job_name, report_num) VALUES (?,?,?,?,?)''',
                (emp_id, log_date, hours, job, report_num))
    con.commit()
    print('Inserted row')
    cur.close()
    return con
  except Exception as e:
    exception_handler(con, e, "Skipping row")

def get_records_sorted(con):
  cur = con.cursor()
  try:
    cur.execute('''SELECT employee_id as employeeId, log_date, (hours * rate) AS amountPaid FROM EMPLOYEE_LOGS INNER JOIN JOBS WHERE EMPLOYEE_LOGS.job_name = JOBS.name ORDER BY employee_id ASC, log_date ASC''')
    rows = cur.fetchall()
    cur.close()
    return rows
  except Exception as e:
    exception_handler(con, e, "Cannot continue since report generation failed on db")

def exists_report(con, report_num):
  cur = con.cursor()
  try:
    cur.execute('''SELECT report_num FROM EMPLOYEE_LOGS WHERE report_num=? LIMIT 1''', (report_num,))
    rows = cur.fetchall()
    cur.close()
    if not rows:
      return False
    return True # should be true
  except Exception as e:
    exception_handler(con, e, "Cannot continue since checking if report num exists failed on db")


if __name__ == "__main__":
  args = sys.argv[1:]
  if not args or len(args) > 1 or args[0] not in ['init', 'migrate']:
    print("Usage: python db.py [init|migrate]")
    exit(1)

  if args[0] == 'init':
    initialize_db('example.db')
  else:
    migrate_db('example.db')



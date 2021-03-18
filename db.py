import sqlite3 as sql


def initialize_db(filename):
  con, cur = None, None

  try:
    con = sql.connect(filename)
    cur = con.cursor()

    # create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEE (
    id INTEGER PRIMARY KEY
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS JOB (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rate INTEGER NOT NULL
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEE_LOG (
    employee_id INTEGER NOT NULL,
    log_date DATE NOT NULL,
    hours INTEGER NOT NULL,
    job_name TEXT NOT NULL,
    report_num TEXT NOT NULL,
    FOREIGN KEY (employee_id)
      REFERENCES EMPLOYEE(id),
    FOREIGN KEY (job_name)
      REFERENCES JOB(name)
    )''')

    con.commit()
  except Exception as e:
    if con:
      con.rollback()

    print(f"Unexpected error. Cannot continue: {e.args[0]}")
    exit(1)
  finally:
    if con:
      con.close()

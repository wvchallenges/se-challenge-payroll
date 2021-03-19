import sys

import db_helpers


def initialize_db():
  con = None

  try:
    con = db_helpers.get_connection()
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
    db_helpers.exception_handler(con, e, "Cannot continue since db init failed")
    exit(1)


def migrate_db():
  con = None

  try:
    con = db_helpers.get_connection()
    cur = con.cursor()

    cur.execute('''DELETE FROM JOBS''')
    cur.execute('''INSERT INTO JOBS (name, rate) VALUES (?,?)''', ('A', 20,))
    cur.execute('''INSERT INTO JOBS (name, rate) VALUES (?,?)''', ('B', 30,))

    con.commit()
    cur.close()
    print("Database rows migrated!")
    return con
  except Exception as e:
    db_helpers.exception_handler(con, e,
                                 "Cannot continue since db migration failed")
    exit(1)


if __name__ == "__main__":
  args = sys.argv[1:]
  if not args or len(args) > 1 or args[0] not in ['init', 'migrate']:
    print("Usage: python db.py [init|migrate]")
    exit(1)

  if args[0] == 'init':
    initialize_db()
  else:
    migrate_db()

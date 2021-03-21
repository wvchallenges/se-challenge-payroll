import sqlite3 as sql
import os

# will get created in backend folder
DB_FILENAME = "example.db"

def exception_handler(con, e, msg):
  # if exception occured in db transaction, roll it back if possible
  if con:
    print("Rolling back changes")
    con.rollback()

  # throw exception to main thread so we can return to user
  if e:
    raise Exception(f"Unexpected error. {msg}: {e.args[0]}")
  raise Exception(f"Unexpected error. {msg}")

def get_connection():
  # connect to the db, this happens a total of 3 times
  # once with db init, once with db migrate, and then with flask run
  con = None

  try:
    con = sql.connect(DB_FILENAME, check_same_thread=False)
    return con
  except Exception as e:
    exception_handler(con, e, "Cannot continue since db connect failed")
    exit(1)

def delete_db():
  # remove db file if exists
  try:
    if os.path.isfile(DB_FILENAME):
      os.remove(DB_FILENAME)
  except Exception as e:
    raise Exception(f"Unable to delete db file: {e}")
    exit(1)


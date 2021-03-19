import sqlite3 as sql

DB_FILENAME = "example.db"

def exception_handler(con, e, msg):
  if con:
    con.rollback()

  if e:
    raise Exception(f"Unexpected error. {msg}: {e.args[0]}")
  raise Exception(f"Unexpected error. {msg}")

def get_connection():
  con = None

  try:
    con = sql.connect(DB_FILENAME, check_same_thread=False)
    return con
  except Exception as e:
    exception_handler(con, e, "Cannot continue since db connect failed")
    exit(1)

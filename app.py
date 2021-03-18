import re

import db
import csv
import os

def main():
  con = db.initialize_db('example.db')
  read_csv('time-report-42.csv', con)

def read_csv(csv_file, con):
  report_num = re.findall(r"time-report-(\d+)\.csv",csv_file)[0]
  with open(csv_file) as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        print(f'Column names are {", ".join(row)}')
      else:
        db.insert_csv_row(con, row, report_num)
      line_count += 1

if __name__ == "__main__":
  os.remove('example.db')
  main()

# http://www.sqlitetutorial.net/sqlite-python/creating-database/
# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python

import sqlite3
from sqlite3 import Error
import csv

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (Show name, Network, Runtime in minutes, Seasons, On/Off air, Genre);")

with open('tv_tuner_data.csv') as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Show name'], i['Network'], i['Runtime in minutes'], i['Seasons'], i['On/Off air'], i['Genre'])
             for i in dr]

cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    create_connection("tv_tuner.db")
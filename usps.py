from dbi import create_connection, create_table
import csv

# Temporary file... only needed to put the data into the database

def read_and_enter():
    conn = create_connection("fulldata.sqlite")
    create_table(conn)
    cur = conn.cursor()
    file = open("collection_boxes_2020-08-19.csv")
    rows = csv.reader(file)
    cur.executemany("INSERT INTO usps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    conn.commit()
    conn.close()

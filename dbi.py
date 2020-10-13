import sqlite3 as sql
from sqlite3 import Error

def create_connection(db_filename):
    conn = None
    try:
        conn = sql.connect(db_filename)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    command = """CREATE TABLE IF NOT EXISTS usps (id text PRIMARY KEY, streetaddress TEXT, city text, state text, zip text, collection1 text, collection2 text, collection3 text, collection4 text, collection5 text, collection6 text, collection7 text, latitude text, longitude text)"""
    try:
        cur = conn.cursor()
        cur.execute(command)
    except Error as e:
        print(e)

def create_table_votelinks(conn):
    command = """CREATE TABLE IF NOT EXISTS voterlinks (state text PRIMARY KEY, voter text, mailin text, status text)"""
    try:
        cur = conn.cursor()
        cur.execute(command)
    except Error as e:
        print(e)


def select_from_zip(conn, zip):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usps WHERE zip=?", (zip,))
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)


def select_from_id(conn, id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usps WHERE id=?", (id,))
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)
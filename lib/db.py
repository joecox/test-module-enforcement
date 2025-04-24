import sqlite3

DB_FILE = "db.sqlite3"


def connection():
    return sqlite3.connect(DB_FILE)  # noqa: TID251

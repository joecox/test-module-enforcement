from contextlib import asynccontextmanager
import sqlite3
from uuid import uuid4

from fastapi import FastAPI

DB_FILE = "db.sqlite3"


def load_data():
    con = sqlite3.connect(DB_FILE)  # noqa: TID251
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS providers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            npi TEXT NOT NULL,
            profession TEXT NOT NULL
        )
        """
    )
    con.executemany(
        """
        INSERT INTO providers (id, name, npi, profession)
        VALUES (?, ?, ?, ?)
        """,
        [
            (str(uuid4()), "Pizza Man", "1134225618", "DC"),
            (str(uuid4()), "Whitaker Smith", "1003827205", "MD"),
            (str(uuid4()), "Horace Williams", "1083169015", "RPh"),
        ],
    )
    con.commit()
    con.close()


def destroy_data():
    con = sqlite3.connect(DB_FILE)  # noqa: TID251
    con.execute("DROP TABLE IF EXISTS providers")
    con.commit()
    con.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()
    yield
    destroy_data()

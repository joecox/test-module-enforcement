from typing import TYPE_CHECKING
from uuid import UUID
from lib.db import connection
from lib.logging import log
from providers.model import Provider

if TYPE_CHECKING:
    from sqlite3 import Cursor


def provider_row_factory(_cursor: Cursor, row: tuple[str, str, str, str]) -> Provider:
    return Provider(
        id=UUID(row[0]),
        name=row[1],
        npi=row[2],
        profession=row[3],
    )


def get_providers() -> list[Provider]:
    with connection() as con:
        con.row_factory = provider_row_factory
        return con.execute("SELECT * FROM providers").fetchall()


def get_provider(id: UUID) -> Provider | None:
    log("get_provider")
    with connection() as con:
        con.row_factory = provider_row_factory
        return con.execute("SELECT * FROM providers WHERE id = ?", [str(id)]).fetchone()

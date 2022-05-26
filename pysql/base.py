from __future__ import annotations

from typing import TYPE_CHECKING, List

from .model import Model
from .session import Session
from .query import Query

if TYPE_CHECKING:
    from .metadata import MetaData
    from .table import Table

__all__: List[str] = [
    'PySQL'
]


class PySQL:

    Model: Model = Model
    session: Session = Session
    query: Query = Query

    def __init__(
        self,
        engine: str,
        connection,
        meta: MetaData
    ) -> None:

        engines = ('postgresql', 'sqlite3', 'mysql')

        if engine not in engines:
            raise ValueError(f"'{engine}' not in {engines}")

        self.engine: str = engine
        self.connection = connection

        self.meta: MetaData = meta
        self.meta.execute = self.execute
        self.meta.schema.meta = self.meta

        self.Model.meta = self.meta
        self.Model.engine = self.engine
        self.Model.mark = {
            'postgresql': '%s',
            'sqlite3': '?',
            'mysql': '%s'
        }

        self.session.connection = self.connection
        self.query.connection = self.connection

        return None

    def get_table(self, __table_name: str, /) -> Table:

        return self.meta.tables[__table_name]

    def execute(self, sql: str, /) -> None:

            self.connection.cursor().execute(sql)
            self.connection.commit()

            return None

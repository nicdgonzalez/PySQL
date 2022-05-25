from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional

from .column import Column

if TYPE_CHECKING:
    from .metadata import MetaData

__all__: List[str] = [
    'Table'
]


class Table:
    """Represents a schema table in the database."""

    description: str

    def __init__(
        self,
        name: str,
        meta: MetaData,
        columns: Iterable[Column] = (),
        constraints: Optional[Iterable[str]] = (),
        inherit: Optional[Table] = None
    ) -> None:

        self.name: str = f'"{name}"'
        self.meta: MetaData = meta

        if (self.meta.schema.name):
            self.name = f'"{self.meta.schema.name}".{self.name}'

        self.columns: Iterable[Column] = columns
        for (column) in self.columns:
            column.table = self

        self.constraints: List[str] = constraints
        self.inherit: Table = inherit

        self.meta.info[self.name] = self._to_metadata()

        return None

    @property
    def table_name(self) -> str:

        return (
            self.name
            .replace('"', '')
            .rsplit('.', maxsplit=1)
            [-1]
        )

    def _to_metadata(self) -> dict:

        return {
            'table_name': self.table_name,
            'columns': {
                index: column._to_metadata()
                for (index, column)
                in enumerate(self.columns)
            },
            'constraints': self.constraints
        }

    def create(self) -> str:
        """:class:`str` Returns the SQL statement to execute this command."""

        sql: List[str] = [f'CREATE TABLE IF NOT EXISTS {self.name} (']
        columns: List[str] = []

        # If more than one column in self.columns has Primary Key set to True,
        # then the constraint must be set as a Table constraint.
        primary_key_columns: List[str] = [
            column.name
            for column in self.columns
            if column.primary_key
        ]
        pk_is_table_constraint: bool = (len(primary_key_columns) > 1)

        for (column) in self.columns:
            if not isinstance(column, Column):
                continue

            base: str = f'{column.name} {column.data_type.name}'

            if (column.not_null):
                base += ' NOT NULL'

            if (column.primary_key) and (not pk_is_table_constraint):
                base += ' PRIMARY KEY'

            if (column.reference):
                base += f' {str(column.reference)}'

                if (column.on_delete):
                    base += f' ON DELETE {column.on_delete}'

                if (column.on_update):
                    base += f' ON UPDATE {column.on_update}'

            if (column.default):
                base += f' DEFAULT {column.default}'

            if (column.check):
                base += f' CHECK ({column.check})'

            columns.append(base)

        if (pk_is_table_constraint):
            sql_pkey: str = f"PRIMARY KEY ({', '.join(primary_key_columns)})"
            self.constraints = sql_pkey
            columns.append(sql_pkey)

        sql.append(f"{', '.join(columns)} )")

        if (self.inherit):
            sql.append(f' INHERITS ({self.inherit.name})')

        sql: str = (' '.join(sql))

        return self.meta.execute(sql)

    def drop(self) -> str:
        """:class:`str` Returns the SQL statement to execute this command."""

        sql: str = f'DROP TABLE IF EXISTS {self.name};'

        return self.meta.execute(sql)

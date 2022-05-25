from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Tuple

if TYPE_CHECKING:
    from .model import Model


class Query:

    __slots__: Tuple[str, ...] = ()

    @classmethod
    def fetchone(
        cls,
        model: Model,
        select: List[str] = ['*']
    ) -> Tuple[Any, ...]:

        cursor = cls._fetch(model=model, select=select)

        return cursor.fetchone()

    @classmethod
    def fetchmany(
        cls,
        model: Model,
        select: List[str] = ['*']
    ) -> List[Tuple[Any, ...]]:

        cursor = cls._fetch(model=model, select=select)

        return cursor.fetchmany()

    @classmethod
    def fetchall(
        cls,
        model: Model,
        select: List[str] = ['*']
    ) -> List[Tuple[Any, ...]]:

        cursor = cls._fetch(model=model, select=select)

        return cursor.fetchall()

    @classmethod
    def _execute(cls, sql: str, val: Tuple[Any, ...] = None) -> Any:
        """[Internal Method]"""

        cursor = cls.connection.cursor()
        (
            cursor.execute(sql, val)
            if val
            else cursor.execute(sql)
        )

        return cursor

    @classmethod
    def _fetch(cls, model: Model, select: List[str] = ['*']) -> Any:
        """[Internal Method]"""

        table_name: str = model.table.name
        mark: str = model.mark[model.engine]

        base_filter: str = 'WHERE '
        base_filter_copy: str = base_filter
        values: List[str] = []

        column_names: List[str] = list(model.kwargs.keys())
        if len(column_names) > 0:
            for fltr_name in column_names:
                value: Any = model.kwargs[fltr_name]
                if value is not None:
                    base_filter += f'{fltr_name} = {mark} AND '
                    values.append(value)

        columns: str = (', ').join(select)
        sql: str = f'SELECT {columns} FROM {table_name}'

        if (base_filter != base_filter_copy):
            sql_filter: str = base_filter.strip('AND ')
            sql += (' ' + sql_filter)

        val: Tuple[Any, ...] = tuple(values)

        return cls._execute(sql, val)

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Tuple

if TYPE_CHECKING:
    from .model import Model


class Session:

    __slots__: Tuple[str, ...] = ()

    @classmethod
    def insert(cls, model: Model) -> None:

        table_name: str = model.table.name
        mark: str = model.mark[model.engine]

        column_names: List[str] = list(model.kwargs.keys())
        values: List[Any] = list(model.kwargs.values())

        columns: str = (', ').join(column_names)
        marks: str = (f'{mark}, ' * len(column_names)).strip(', ')

        sql: str = f'INSERT INTO {table_name}({columns}) VALUES({marks});'
        val: Tuple[Any] = tuple(values)

        return cls._execute(sql, val)

    @classmethod
    def update(cls, model: Model, filter: dict = None) -> None:

        table_name: str = model.table.name
        mark: str = model.mark[model.engine]

        base_update: str = ''
        values: List[Any] = []

        columns: Dict[str, Any] = model.kwargs
        for name in columns.keys():
            base_update += f'{name} = {mark}, '
            values.append(columns[name])

        base_filter: str = 'WHERE '
        base_filter_copy: str = base_filter

        if filter is not None:
            for fltr_name in filter.keys():
                value: Any = filter[fltr_name]
                if value is not None:
                    base_filter += f'{fltr_name} = {mark} AND '
                    values.append(value)

        sql_update: str = base_update.strip(', ')
        sql: str = f'UPDATE {table_name} SET {sql_update}'

        if base_filter != base_filter_copy:
            sql_filter: str = base_filter.strip('AND ')
            sql += (' ' + sql_filter)

        val: Tuple[Any] = tuple(values)

        return cls._execute(sql, val)

    @classmethod
    def delete(cls, model: Model) -> None:

        table_name: str = model.table.name
        mark: str = model.mark[model.engine]

        base_filter = 'WHERE '
        base_filter_copy = base_filter
        values: List[Any] = []

        for fltr_name in list(model.kwargs.keys()):
            value: Any = model.kwargs[fltr_name]
            if value is not None:
                base_filter += f'{fltr_name} = {mark} AND '
                values.append(value)

        sql: str = f'DELETE FROM {table_name}'

        if base_filter != base_filter_copy:
            sql_filter: str = base_filter.strip('AND ')
            sql += (' ' + sql_filter)

        val: Tuple[Any, ...] = tuple(values)

        return cls._execute(sql, val)

    @classmethod
    def _execute(cls, sql: str, val: Tuple[Any, ...] = None) -> None:
        """[Internal Method]"""

        cursor = cls.connection.cursor()
        (
            cursor.execute(sql, val)
            if (val is not None)
            else cursor.execute(sql)
        )
        cls.connection.commit()

        return None

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from .column import Column
from .table import Table

if TYPE_CHECKING:
    from .metadata import MetaData

__all__: List[str] = [
    'Model'
]


class ModelBase(type):

    def __new__(
        cls,
        __name: str,
        __bases: Tuple[type, ...],
        __attrs: Dict[str, Any],
        **kwargs
    ) -> type:

        columns: List[Column] = []

        for (name, column) in __attrs.items():
            if not isinstance(column, Column):
                continue

            column.name = name
            columns.append(column)

        __attrs['columns'] = columns

        return super().__new__(cls, __name, __bases, __attrs, **kwargs)


class Model(metaclass=ModelBase):

    meta: MetaData

    def __init_subclass__(
        cls,
        name: Optional[str] = None,
        inherit: Optional[Table] = None
    ) -> None:

        cls.table_name: str = name if name else cls.__name__

        cls.table: Table = Table(
            name=cls.table_name,
            meta=cls.meta,
            columns=cls.columns,
            inherit=inherit
        )
        cls.table.description = cls.__doc__.strip() if cls.__doc__ else ''

        try:
            cls.meta.tables[cls.table.name]
        except (KeyError,):
            cls.table.create()
            cls.meta.tables[cls.table.name] = cls.table

        return None

    def __init__(self, **columns) -> None:

        self.kwargs: Dict[str, Any] = columns

        return None

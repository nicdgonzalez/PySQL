from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from .constraints import ForeignKey
from .datatype import DataType

if TYPE_CHECKING:
    from .table import Table

__all__: List[str] = [
    'Column',
    'NO_ACTION',
    'CASCADE',
    'RESTRICT'
]

NO_ACTION: str = 'NO ACTION'
CASCADE: str = 'CASCADE'
RESTRICT: str = 'RESTRICT'


class Column:
    """Represents a table column in the database."""

    table: Table  # The table this column belongs to.

    def __init__(
        self,
        __name: Optional[str] = None,
        __data_type: Optional[DataType] = None,
        /,
        *,
        name: str = None,
        data_type: DataType = None,
        not_null: bool = False,
        primary_key: bool = False,
        reference: Optional[Column] = None,
        on_delete: Optional[str] = None,
        on_update: Optional[str] = None,
        default: Optional[Any] = None,
        check: Optional[str] = None
    ) -> None:

        pos_args: list = [a for a in (__name, __data_type) if (a is not None)]

        error: str = "'%s' is defined in positional and keyword argument."
        if (pos_args):
            if isinstance(pos_args[0], str):
                if (name is not None):
                    raise Exception(error % ('name'))
                name = pos_args.pop(0)
            elif isinstance(pos_args[0], DataType):
                if (data_type is not None):
                    raise Exception(error % ('datatype'))
                data_type = pos_args.pop(0)

        if (pos_args):
            if isinstance(pos_args[0], DataType):
                if (data_type is not None):
                    raise Exception(error % ('datatype'))    
                data_type = pos_args[0]

        if (reference) and (not isinstance(reference, ForeignKey)):
            if isinstance(reference, Column):
                reference = ForeignKey(reference)
            else:
                error: str = "Parameter '%s' must be of type :class:`%s`."
                raise TypeError(error % ('reference', 'ForeignKey'))

        self.name: str = name
        self.data_type: DataType = data_type
        self.not_null: bool = not_null
        self.primary_key: bool = primary_key
        self.reference: ForeignKey = reference
        self.on_delete: str = on_delete
        self.on_update: str = on_update
        self.default: Any = (
            f"'{default}'"
            if isinstance(default, str)
            else default
        )
        self.check: str = check

        return None

    def _to_metadata(self) -> dict:

        return {
            'column_name': self.name,
            'data_type': self.data_type.name,
            'constraints': {
                'nullable': False if self.not_null else True,
                'primary_key': self.primary_key,
                'foreign_key': {
                    'reference': str(self.reference),
                    'on_delete': self.on_delete,
                    'on_update': self.on_update,
                } if self.reference else None,
                'default_value': self.default,
                'check': self.check
            }
        }

    def rename(self, new_name: str) -> str:

        sql: List[str] = [
            f'ALTER TABLE IF EXISTS {self.table.name}',
            f'RENAME COLUMN "{self.name}" TO "{new_name}"'
        ]

        sql: str = ' '.join(sql)
        self.name = new_name

        return self.table.meta.execute(sql)

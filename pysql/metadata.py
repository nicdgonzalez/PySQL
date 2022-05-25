from __future__ import annotations

from json import dump, load
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar

from .schema import Schema
from .utils import PYSQL_ROOT

if TYPE_CHECKING:
    from .table import Table

__all__: List[str] = [
    'MetaData'
]

PATH_METADATA_JSON: str = f'{PYSQL_ROOT}/tmp/cache/metadata.json'

_DefaultSchema: Schema = Schema(name=None)


# Work in Progress:
# To store the state of the the model and check for any changes.
class MetaDataInfo(dict):

    def __init__(self) -> None:

        self.file: str = PATH_METADATA_JSON
        self.data: dict = {}

        return super().__init__()

    def __setitem__(self, key, value) -> None:

        self.data[key] = value

        with open(self.file, 'w+') as fp:
            dump(self.data, fp, indent=4)

        return super().__setitem__(key, value)


class MetaData:

    info: Dict[str, Any] = MetaDataInfo()
    tables: Dict[str, Table] = {}

    def __init__(
        self,
        schema: Optional[Schema] = _DefaultSchema
    ) -> None:

        self.schema: Schema = schema
        self.info  # Updates the 'metadata.json' file.

        return None

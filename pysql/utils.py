from json import load
from pathlib import Path
from typing import List
from urllib.parse import quote as uri_quote

__all__: List[str] = [
    'config_to_dsn'
]

PYSQL_ROOT: str = str(Path(__file__).parents[0]).replace('\\', '/')


def config_to_dsn(**config) -> str:

    return (
        '{engine}://{user}:{password}@{host}:{port}/{database}'
        .format(**{k: uri_quote(str(v)) for (k, v) in config.items()})
    )

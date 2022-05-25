from typing import List, Optional

__all__: List[str] = [
    'Schema'
]


class Schema:
    """Represents a schema in the database."""

    def __init__(
        self,
        name: str = None
    ) -> None:

        self.name: str = name

        return None

    def create(
        self,
        name: Optional[str] = None,
        authorization: Optional[str] = None
    ) -> None:

        sql: List[str] = ['CREATE SCHEMA']

        if not any(name, authorization):
            error: str = "Atleast (1) parameter ('%s', '%s') must be defined."
            raise TypeError(error % ('name', 'authorization'))

        if name:
            sql.append(f'"{name}"')

        if authorization:
            if not name:
                name = authorization
                sql.append(f'"{name}"')
            sql.append(f'AUTHORIZATION "{authorization}"')

        return self.meta.execute(f"{' '.join(sql)};")

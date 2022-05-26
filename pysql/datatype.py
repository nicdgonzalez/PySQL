from typing import List, Tuple

__all__: List[str] = [
    'BigInt',
    'Blob',
    'Boolean',
    'Char',
    'Datetime',
    'Integer',
    'Numeric',
    'Real',
    'Serial',
    'Text',
    'VarChar'
]


class DataType:

    __slots__: Tuple[str, ...] = ('name')

    def __init__(self, name: str, /, *args) -> None:

        self.name: str = f'{name}'

        if (args):
            self.name += f"({', '.join(args)})"

        return None


BigInt: DataType = DataType('BigInt')
Blob: DataType = DataType('Blob')
Boolean: DataType = DataType('Boolean')
Char: DataType = lambda n: DataType('Character', n)
Datetime: DataType = DataType('Datetime')
Integer: DataType = DataType('Integer')
Numeric: DataType = DataType('Numeric')
Real: DataType = DataType('Real')
Serial: DataType = DataType('Serial')
Text: DataType = DataType('Text')
VarChar: DataType = lambda n: DataType('Character Varying', n)

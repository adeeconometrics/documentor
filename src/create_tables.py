from typing import Dict, List, Any, Tuple
from enum import Enum, auto

from pydantic import BaseModel, field_validator
from tabulate import tabulate


def enum_factory(enum_name: str, names: Tuple[str, ...]) -> Enum:
    """Create an Enum class with the given name and names."""
    TEnumClass = Enum(enum_name, {name: name for name in names})
    return TEnumClass


TableFmt: Enum = enum_factory('TableFmt', ('plain', 'simple', 'github', 'grid', 'fancy_grid', 'pipe', 'orgtbl', 'jira', 'presto', 'pretty',
                        'psql', 'rst', 'mediawiki', 'moinmoin', 'youtrack', 'html', 'unsafehtml', 'latex', 'latex_raw', 'latex_booktabs', 'textile'))


class TableData(BaseModel):
    """Represents a table of data."""
    mapping: Dict[str, List[Any]]

    @field_validator('mapping')
    def validate_lengths(cls, mapping: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Validate that all values in the mapping have the same length."""
        for key, values in mapping.items():
            if len(values) != len(mapping[next(iter(mapping))]):
                raise ValueError(
                    f"Length of {key} does not match other columns")
        return mapping


def make_table(table: TableData, tbl_format: Enum = TableFmt.mediawiki) -> str:
    """Convert the table to a table string."""
    return tabulate(table.mapping, headers="keys", tablefmt=tbl_format.value)


if __name__ == '__main__':
    data = TableData(mapping={
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [30, 45, 25],
        "City": ["New York", "Los Angeles", "Chi"]
    })
    print(make_table(data))

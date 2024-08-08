from typing import Dict, List, Any
from enum import Enum, auto

from pydantic import BaseModel, field_validator
from tabulate import tabulate

class TableFmt(Enum):
    """Represents the format of the table."""
    
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name
    
    plain = auto()
    simple = auto()
    github = auto()
    grid = auto()
    simple_grid = auto()
    rounded_grid = auto()
    heavy_grid = auto()
    mixed_grid = auto()
    double_grid = auto()
    fancy_grid = auto()
    outline = auto()
    simple_outline = auto()
    rounded_outline = auto()
    heavy_outline = auto()
    mixed_outline = auto()
    double_outline = auto()
    fancy_outline = auto()
    pipe = auto()
    orgtbl = auto()
    asciidoc = auto()
    jira = auto()
    presto = auto()
    pretty = auto()
    psql = auto()
    rst = auto()
    mediawiki = auto()
    moinmoin = auto()
    youtrack = auto()
    html = auto()
    unsafehtml = auto()
    latex = auto()
    latex_raw = auto()
    latex_booktabs = auto()
    latex_longtable = auto()
    textile = auto()
    tsv = auto()


class TableData(BaseModel):
    """Represents a table of data."""
    mapping: Dict[str, List[Any]]

    @field_validator('mapping')
    def validate_lengths(cls, mapping: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Validate that all values in the mapping have the same length."""
        for key, values in mapping.items():
            if len(values) != len(mapping[next(iter(mapping))]):
                raise ValueError(f"Length of {key} does not match other columns")
        return mapping

def make_table(table:TableData, tbl_format:TableFmt = TableFmt.github) -> str:
    """Convert the table to a table string."""
    return tabulate(table.mapping, headers="keys", tablefmt=tbl_format.value)

if __name__ == '__main__':
    data = TableData(mapping={
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [30, 45, 25],
        "City": ["New York", "Los Angeles", "Chi"]
    })
    print(make_table(data))
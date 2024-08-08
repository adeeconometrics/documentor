from typing import Dict, List, Any, Tuple, Union
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, field_validator
from tabulate import tabulate
from faker import Faker

fake = Faker()

def enum_factory(enum_name: str, names: Tuple[str, ...]) -> Enum:
    """Create an Enum class with the given name and names. 
    Note that this is restricted to string-types names."""
    return Enum(enum_name, {name: name for name in names})



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


def make_table(table: TableData, tbl_format: Enum = TableFmt.github) -> str:
    """Convert the table to a table string."""
    return tabulate(table.mapping, headers="keys", tablefmt=tbl_format.value)

def save_tbl_to_file(table: TableData, file_path: Union[Path,str], tbl_format: Enum = TableFmt.github) -> None:
    """Save the table to a file."""
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write(make_table(table, tbl_format))

if __name__ == '__main__':

    words_list:tuple[str,...] = (
        "Compute", "Storage", "Network", "Virtual", "Machine", "Disk", "Blob", "Queue", "Table", "File",
        "Container", "Resource", "Group", "KeyVault", "Identity", "Function", "Logic", "App", "Service", "API",
        "Gateway", "Endpoint", "Subnet", "Firewall", "LoadBalancer", "ScaleSet", "VNet", "Traffic", "Manager", "CDN",
        "Instance", "Cluster", "Namespace", "Policy", "Role", "Binding", "Certificate", "Automation", "Runbook", "Hybrid",
        "Connector", "Event", "Hub", "Stream", "Analytics", "Data", "Lake", "Factory", "Synapse", "Pipeline",
        "Trigger", "Monitor", "Alert", "Log", "Insights", "Metric", "Dashboard", "Workspace", "Backup", "Recovery",
        "Site", "Advisor", "Cost", "Management", "Billing", "Compliance", "Security", "Center", "AzureAD", "Bastion",
        "DevOps", "Pipeline", "Artifact", "Release", "Repository", "Board", "Wiki", "Test", "Agent", "Pool",
        "Environment", "Secret", "Access", "Control", "Route", "Table", "Uptime", "SLA", "Latency", "Throughput",
        "Cache", "Redis", "SQL", "MySQL", "PostgreSQL", "CosmosDB", "MongoDB", "Backup", "Archive", "Tier"
    )
    data = TableData(mapping={
        'parameter': ['_'.join( word.lower() for word in 
                               fake.words(nb=3, ext_word_list=words_list)) for _ 
                               in range(20)],
        'value': [fake.sentence() for _ in range(20)],
    })
    save_tbl_to_file(data, Path('./data/data.md'), TableFmt.github)
    print(make_table(data))

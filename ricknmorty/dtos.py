
from dataclasses import dataclass


@dataclass
class JsonItem:
    id: str
    metadata: str
    raw: dict

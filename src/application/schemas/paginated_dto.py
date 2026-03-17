from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass
class PaginatedDto(Generic[T]):
    items: list[T]
    total_items: int
    page: int
    page_size: int
    total_pages: int

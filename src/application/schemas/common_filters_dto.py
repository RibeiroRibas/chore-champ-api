from dataclasses import dataclass


@dataclass
class CommonFiltersDto:
    page_size: int
    page: int

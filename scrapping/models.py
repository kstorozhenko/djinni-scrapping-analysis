from dataclasses import dataclass


@dataclass
class Vacancy:
    title: str
    company: str
    location: str
    requirements: list
    views_count: int
    reviews_count: int

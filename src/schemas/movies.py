from pydantic import BaseModel, ConfigDict, field_validator
import datetime
from typing import Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)

    @field_validator("budget", "revenue", mode="before")
    def cast_to_int(cls, v):
        if v in (None, ""):
            return 0
        try:
            return int(float(v))
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for budget/revenue: {v!r}")


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)

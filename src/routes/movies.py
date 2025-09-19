from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db, MovieModel
from src.schemas import MovieListResponseSchema, MovieDetailResponseSchema
from typing import Optional

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Retrieve a paginated list of movies."""

    total_items = await db.execute(
        select(func.count()).select_from(MovieModel)
    )
    total_items = int(total_items.scalar_one())

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_url = "/theater/movies/"
    prev_page: Optional[str] = None
    next_page: Optional[str] = None

    if page > 1:
        prev_page = f"{base_url}?page={page-1}&per_page={per_page}"
    if page < total_pages:
        next_page = f"{base_url}?page={page+1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int, db: AsyncSession = Depends(get_db)
) -> MovieModel:
    """Retrieve a single movie by its ID."""
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return movie

from datetime import datetime

from pydantic import BaseModel, Field


class BlogPostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    summary: str = Field(min_length=10, max_length=240)
    content: str = Field(min_length=30)
    author: str = Field(min_length=2, max_length=60)


class BlogPostResponse(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    author: str
    created_at: datetime

    class Config:
        from_attributes = True

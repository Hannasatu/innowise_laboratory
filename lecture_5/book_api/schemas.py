# schemas.py
from pydantic import BaseModel, Field
from typing import Optional


# Базовая схема для книги (общие поля)
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1000, le=9999)


# Схема для создания новой книги (наследует BookBase)
class BookCreate(BookBase):
    pass


# Схема для обновления книги (все поля опциональны)
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=9999)


# *** УБЕДИТЕСЬ, ЧТО ЭТОТ КЛАСС ПРИСУТСТВУЕТ И ПРАВИЛЬНО НАЗВАН ***
class Book(BookBase):
    id: int

    class Config:
        from_attributes = True  # Для pydantic v2+
        # orm_mode = True # Для pydantic v1.x (если используете старую версию)


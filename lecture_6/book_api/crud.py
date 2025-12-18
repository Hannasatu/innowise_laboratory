from sqlalchemy.orm import Session
import models, schemas
from typing import List, Optional

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True

def update_book(db: Session, book_id: int, book: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    db.commit()
    db.refresh(db_book)
    return db_book

def search_books(db: Session, title: str = None, author: str = None, year: int = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(models.Book.year == year)
    return query.all()

# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, database


app = FastAPI(
    title="Book API",
    description="A simple API for managing books with CRUD and search functionality.",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)


@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):

    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")


    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book



@app.get("/books/search/", response_model=List[schemas.Book])
def search_books(
        q: Optional[str] = Query(None, min_length=1, max_length=50,
                                 description="Search query for title, author, or year"),
        db: Session = Depends(database.get_db)
):
    if not q:

        return []

    query = db.query(models.Book)
    search_term = f"%{q.lower()}%"
    query = query.filter(
        (models.Book.title.ilike(search_term)) |
        (models.Book.author.ilike(search_term)) |
        (models.Book.year.like(search_term)) )

    books = query.all()
    return books

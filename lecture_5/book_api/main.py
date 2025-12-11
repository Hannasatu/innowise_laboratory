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

# --- Эндпоинты API ---

# POST /books/ - Добавить новую книгу
@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.model_dump()) # Создаем ORM-объект из Pydantic-модели
    db.add(db_book) # Добавляем в сессию
    db.commit() # Сохраняем изменения в БД
    db.refresh(db_book) # Обновляем объект, чтобы получить сгенерированный ID
    return db_book

# GET /books/ - Получить все книги
@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # Добавлена простая пагинация (skip, limit)
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

# GET /books/{book_id} - Получить книгу по ID (не указано в задании, но полезно для PUT/DELETE)
@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# DELETE /books/{book_id} - Удалить книгу по ID
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book) # Удаляем объект из сессии
    db.commit() # Сохраняем изменения
    return {"message": "Book deleted successfully"} # FastAPI вернет 204 без тела

# PUT /books/{book_id} - Обновить детали книги по ID
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Обновляем поля книги только если они предоставлены в запросе
    book_data = book.model_dump(exclude_unset=True)  # Игнорируем поля, которые не были отправлены
    for key, value in book_data.items():
        setattr(db_book, key, value)  # Устанавливаем новые значения

    db.add(db_book)  # Добавляем измененный объект в сессию (не всегда обязательно, но хорошая практика)
    db.commit()  # Сохраняем изменения
    db.refresh(db_book)  # Обновляем объект из БД
    return db_book


# GET /books/search/ - Поиск книг по заголовку, автору или году
@app.get("/books/search/", response_model=List[schemas.Book])
def search_books(
        q: Optional[str] = Query(None, min_length=1, max_length=50,
                                 description="Search query for title, author, or year"),
        db: Session = Depends(database.get_db)
):
    if not q:
        # Если запрос пуст, можно вернуть все книги или ничего
        return []  # Или `return db.query(models.Book).all()` если хотите все по умолчанию

    query = db.query(models.Book)
    search_term = f"%{q.lower()}%"  # Для поиска без учета регистра

    # Фильтрация по title, author, year
    query = query.filter(
        (models.Book.title.ilike(search_term)) |  # `ilike` для поиска без учета регистра
        (models.Book.author.ilike(search_term)) |
        (models.Book.year.like(search_term))  # Для года используем like, он работает и с числами
    )

    books = query.all()
    return books

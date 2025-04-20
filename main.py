from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book
import models, schemas, database

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Book Review API is running!"}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    # Kiểm tra nếu sách đã tồn tại
    db_book = db.query(models.Book).filter(models.Book.title == book.title).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    
    # Tạo đối tượng Book mới
    db_book = models.Book(title=book.title, author=book.author)
    
    # Thêm vào DB và commit
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

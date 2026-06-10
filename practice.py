from pydantic import BaseModel, Field
from typing import List, Optional

class BookCreate(BaseModel):
    """
    
    """
    title:str=Field(
        ...,
        min_length=1,
        description="제목"
    )
    author:str=Field(
        ...,
        min_length=1,
        description="저자"
    )
    price:int = Field(
        ...,
        gt=0,
        description="도서 가격 0 초과"
    )
    category:str=Field(
        "기타",
        description="카테고리"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "",
                "author":"",
                "price": 333,
                "category": "예술"
            }
        }
    }

class BookCreate(BaseModel):
    title:str=Field(
        ...,
        description="홓"
    )
    author:str=Field(
        ...,
        description="햏"
    )
    price:int=Field(
        ...,
        gt=0,
        description="가격"
    )
    category:str=Field(
        "기타",
        description="카테고리"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "제목",
                "author": "저자",
                "price": 3333,
                "category": "예술"
            }
        }
    }

class bookresponse(BaseModel):
    id: int
    title: str
    author: str
    price: int
    category: str

class bookupdate(BaseModel):
    title:Optional[str]=None
    author:Optional[str]=None
    price:Optional[int]=Field(None, gt=0)
    category:Optional[str]=None


from pathlib import Path as FilePath
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.books_schema import BookCreate, BookResponse, BookUpdate

app = FastAPI(
    title="도서관리",
    description="FastAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books_db = {}
next_id = 1

@app.get("/health", summary="서버첵크",tags=["시스템"])
def health_check():
    return {"server":"ok"}

@app.post("/books", response_model=bookresponse, status_code=201, tags=["도서"])
def create_book(book:BookCreate):
    global next_id
    record = {"id":next_id, **book.model_dump()}
    books_db[next_id]=record
    next_id += 1
    return record

@app.get("books", response_model=list[bookresponse], tags=["도서"])
def get_books(
    category:Optional[str]=Query(
        None,
        description="category 필터"
    ),
    author:Optional[str]=Query(
        None,
        description="author 필터"
    )
):
    items = list(books_db.values())
    if category :
        items = [item for item in items if item["category"] in category]
    if author :
        items = [item for item in items if item["author"] in author]
    return items

@app.get("books/{book_id}", response_model=bookresponse, tags=["도서"])
def get_book(
    book_id:int = Path(
        ..., ge=1, description="도서 ID로 도서 검색(ID는 1이상)"
    )
):
    """
        도서 ID로 도서 한건 조회
    """
    if book_id not in books_db :
        raise HTTPException(
            status_code=404,
            detail=f"도서 {book_id}번을 찾을 수 없습니다"
        )
    return books_db[book_id]

@app.put("books/{book_id}", response_model = bookresponse, tags=["도서"])
def update_book(book_id:int, update:bookupdate):
    """
    """
    if book_id not in books_db :
        raise HTTPException(
            status_code=404,
            detail=f"도서{book_id}번을 찾을 수 없습니다"
        )
    
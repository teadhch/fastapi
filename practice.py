
@app.get("/books", response_model=List[BookResponse], tags=["도서"])
def get_books(
    category: Optional[str] = Query(
        None,
        description = "카테고리 필터"
    ),
    author: Optional[str] = Query(None, description = "저자")
):
# ============================================================
# 파일 위치: app/main.py
# 실행 방법: uvicorn app.main:app --reload
# ============================================================
# FastAPI:
# - FastAPI 애플리케이션 객체를 만들 때 사용합니다.
# - 이 객체에 GET, POST, PUT, DELETE 같은 API 주소를 등록합니다.
#

# HTTPException:
# - API 처리 중 오류가 발생했을 때 HTTP 상태 코드와 메시지를 반환할 때 사용합니다.
# - 예: 없는 도서를 조회하면 404 Not Found를 반환합니다.
#

# Path:
# - URL 경로에 포함되는 값을 검증할 때 사용합니다.
# - 예: /books/1 에서 1은 book_id라는 Path Parameter입니다.
#

# Query:
# - URL 뒤에 ?key=value 형태로 붙는 값을 검증할 때 사용합니다.
# - 예: /books?category=프로그래밍 에서 category는 Query Parameter입니다.

from pathlib import Path as FilePath

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field    # 요청 데이터와 응답 데이터의 구조를 정의 할때 사용

# List:
# - 여러 개의 데이터를 리스트 형태로 반환할 때 타입 힌트로 사용합니다.
# - 예: List[BookResponse]는 BookResponse 여러 개를 담은 리스트라는 뜻입니다.
#
# Optional:
# - 값이 있을 수도 있고 없을 수도 있음을 의미합니다.
# - 예: Optional[str]은 문자열이거나 None일 수 있습니다.
from typing import List, Optional   # 데이터를 여러개 담을수 있는 컬렉션 객체

from schemas.books_schema import BookCreate, BookResponse, BookUpdate

# FastAPI 객체 생성
app = FastAPI(
    title="도서관리 API",
    description="FastAPI 기초 실습 - 도서관리 CRUD를 할 수 있는 엔드포인트",
    version="1.0.0"
)

# CORS 설정: 브라우저(프론트엔드)에서 API를 호출할 수 있게 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# frontend 폴더 경로 (프로젝트 루트/frontend)
frontend_dir = FilePath(__file__).resolve().parent.parent / "frontend"

# DB 대신 사용할 딕셔너리
books_db:dict = {}
# 새 도서를 등록할때 사용할 id
next_id = 1

#----------------------------------------------
# 서버 상태 확인용 API
#----------------------------------------------
@app.get("/health", summary="서버 상태 확인", tags=["시스템"])
def health_check() :
    """
    서버가 정상적으로 실행 중인지 확인하는 API입니다.
    실무에서는 health check API를 자주 사용합니다.
    예:
    - 서버 배포 후 정상 실행 여부 확인
    - 로드밸런서가 서버 상태 확인
    - 모니터링 시스템이 주기적으로 호출

    요청:
    GET /health

    응답:
    {
        "status": "ok",
        "version": "1.0.0"
    }
    """
    # 딕셔너리를  FastAPI가 자동으로 json으로 변환한다
    return {"status" : "ok", "version": "1.0.0"}

# 도서등록 (POST /books)
@app.post("/books", response_model=BookResponse, status_code=201, tags=["도서"])
def create_book(book:BookCreate) :
    """
    도서를 등록 합니다.
    status_code=201 : 생성 성공을 의미하는 HTTP 코드
    """
    global next_id 
    # Pydantic 객체를 딕셔너리로 변환후 펼쳐주는 함수
    record = {"id" : next_id, **book.model_dump()}

    books_db[next_id] = record   # 딕셔너리에 record 추가
    next_id += 1
    return record


# 도서검색 (전체 도서목록, 개별 도서 검색)
# 전체도서 검색 (GET /books)
@app.get("/books", response_model=List[BookResponse], tags=["도서"])
def get_books(
    # Query Parameter : URL 뒤에 ?로 붙이는 쿼리스트링(선택적 옵션)
    category: Optional[str] = Query(
        None,
        description="카테고리 필터(예 : ?category=프로그래밍)"
    )
) :
    """
        도서 목록을 조회합니다.
        - ?category=프로그래밍  : 카테고리 필터
    """
    items = list(books_db.values())

    if category :
        items = [book for book in items if book["category"] == category]

    return items

# 개별도서 검색 (GET /books/{book_id})  - books_id : unique한 도서의 번호
@app.get("/books/{book_id}", response_model=BookResponse,  tags=["도서"])
def get_book(
    # Path Parameter : URL 경로에 포함된 값을 얻어올 때 사용
    book_id:int = Path(
        ..., ge=1, description="도서 ID로 도서 검색(ID는 1이상)"
    )
):
    """
        도서 ID로 도서 한건 조회
    """
    if book_id not in books_db :
        raise HTTPException(
            status_code=404,  # not found
            detail=f"도서 {book_id}번을 찾을 수 없습니다"
        )
    return books_db[book_id]


# 도서수정 (PUT /books/{book_id})
@app.put("/books/{book_id}", response_model=BookResponse, tags=["도서"])
def update_book(book_id:int, update:BookUpdate) :
    """
    도서 정보를 수정합니다.
    변경할 필드만 보내도 됩니다. (나머지는 원래 값 유지됨)
    예 : {"price" : 200000}  -> 가격만 변경
    """
    if book_id not in books_db :
        raise HTTPException(
            status_code=404,  # not found
            detail=f"도서 {book_id}번을 찾을 수 없습니다"
        )
    
    # exclude_none=True " None"인 필드 제외
    changes = update.model_dump(exclude_none=True)

    # 딕셔너리의 모든 키를 순회하며 값을 변경
    for k, v in changes.items() :
        books_db[book_id][k] = v   # book_id번 책의 k필드의 값을 v로 변경

    return books_db[book_id]

# 도서삭제 (DELETE /books/{book_id})
@app.delete("/books/{book_id}", status_code=204, tags=["도서"])
def delete_book(book_id:int) :
    """
    {book_id}번 도서를 삭제 합니다
    status_code = 204. 삭제 성공
    """
    if book_id not in books_db :
        raise HTTPException(
            status_code=404,  # not found
            detail=f"도서 {book_id}번을 찾을 수 없습니다"
        )
    
    del books_db[book_id]
    # status_code=204 -> 응답 본문이 없어도 됨.  => return 생략 가능


#----------------------------------------------
# 프론트엔드 페이지 제공 (맨 마지막에 등록)
# - http://127.0.0.1:8000/         → index.html
# - http://127.0.0.1:8000/frontend/ → index.html
#----------------------------------------------
@app.get("/", include_in_schema=False)
def serve_root_page():
    """루트 주소 접속 시 프론트엔드 페이지를 바로 보여줍니다."""
    index_file = frontend_dir / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="frontend/index.html 파일을 찾을 수 없습니다.")
    return FileResponse(index_file)


@app.get("/frontend", include_in_schema=False)
def redirect_frontend():
    """/frontend → /frontend/ 로 이동 (슬래시 없이 접속해도 동작)"""
    return RedirectResponse(url="/frontend/")


# StaticFiles는 반드시 API 라우트 등록 후 맨 마지막에 mount
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


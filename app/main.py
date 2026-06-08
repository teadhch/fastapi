# ============================================================
# 파일 위치: book_api/app/main.py
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

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field   # 요청 데이터와 응답 데이터의 구조를 정의 할때 사용

# List:
# - 여러 개의 데이터를 리스트 형태로 반환할 때 타입 힌트로 사용합니다.
# - 예: List[BookResponse]는 BookResponse 여러 개를 담은 리스트라는 뜻입니다.
#
# Optional:
# - 값이 있을 수도 있고 없을 수도 있음을 의미합니다.
# - 예: Optional[str]은 문자열이거나 None일 수 있습니다.
from typing import List, Optional   # 데이터를 여러개 담을수 있는 컬렉션 객체
from schemas.books_schema import BookCreate, BookResponse

# FastAPI 객체 생성
app = FastAPI(
    title = "도서관리 API",
    description = "FastAPI 기초 실습 - 도서관리 CRUD를 할 수 있는 엔드포인트",
    version = "1.0.0"
)

# 엔드포인트 = 요청할수 있는 주소

# DB 대신 사용할 딕셔너리
books_db:dict = {}
# 새 도서를 등록할때 사용할 id
next_id = 1

#-------------------------------------
# 서버 상태 확인용 API
#-------------------------------------
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
    # 디셔너리를 FastAPI가 자동으로 json으로 변환한다
    return {"status" : "ok", "version" : "1.0.0"}
# 명령어 curl <- 응답을 가져와라? 서버 실행상태에서 실행
# curl "http://127.0.0.1:8000/health"

# 도서등록 (POST /books)
@app.post("/books", response_model=BookResponse, status_code=201, tags=["도서"])
def create_book(book:BookCreate) :
    """
    도서를 등록 합니다
    status_code=201 : 생성 성공을 의미하는 HTTP 코드
    """
    global next_id
    # Pydantic 객체를 딕셔너리로 변환후 펼쳐주는 함수
    record = {"id" : next_id, **book.model_dump()}

    books_db[next_id] = record  # 딕셔너리에 record 추가
    next_id += 1
    return record

# 도서검색 (GET/book)

# 도서수정

# 도서삭제
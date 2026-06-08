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

# FastAPI 객체 생성
app = FastAPI(
    title = "도서관리 API",
    description = "FastAPI 기초 실습 - 도서관리 CRUD를 할 수 있는 엔드포인트",
    version = "1.0.0"
)

# 엔드포인트 요청할수 있는 주소

# DB 대신 사용할 딕셔너리
books_db:dict = {}
# 새 도서를 등록할때 사용할 id
next_id = 1


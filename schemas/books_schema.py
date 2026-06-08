from pydantic import BaseModel, Field
from typing import List, Optional
#------------------------------------------
# 도서 등록 요청 스키마
#------------------------------------------
class BookCreate(BaseModel) :
    """
    도서 등록 요청 스키마입니다.
    이 클래스는 POST /books 요청에서 클라이언트가 보내야 할
    JSON 데이터의 구조를 정의합니다.

    예:
    {
        "title": "파이썬 완전 정복",
        "author": "홍길동",
        "price": 28000,
        "category": "프로그래밍"
    }

    Django의 Form 또는 DRF Serializer와 비슷한 역할입니다.
    """
    title:str = Field(
        ...,    # 필수 요소
        min_length = 1,  # 최소 문자 길이
        max_length = 100,
        description = "도서 제목"
    )

    author:str = Field(
        ...,
        min_length=1,
        description="저자"
    )

    price:int = Field(
        ...,
        gt=0,   # greater than
        description="도서 가격(0초과)"
    )

    category:str = Field(
        "기타", # 기본값 지정 (필수 값이 아니기 때문에 유저가 입력하지 않으면 기본값으로 들어감)
        description = "카테고리 (기본값: 기타)"
    )

    # model_config : Swagger UI에 예시 JSON을 보여주기 위한 설정
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "파이썬 완전 정복",
                "author": "홍길동",
                "price": 28000,
                "category": "프로그래밍"
            }
        }
    }

#-------------------------------------------------
# 도서 응답 스키마 - 도서 검색용 스키마
#-------------------------------------------------
class BookResponse(BaseModel) :
    """
    도서 응답 스키마
    """
    id:int
    title:str
    author:str
    price:int
    category:str

#----------------------------------------------------
# 도서 수정 스키마 - , 수정의 결과용 스키마
#----------------------------------------------------
class BookUpdate(BaseModel) :
    """
    도서 수정시 요청되는 스키마
    모든 필드가 Optional -> 변경할 필드만 전송 되어 수정되도록....
    """
    title:Optional[str] = None
    author:Optional[str] = None
    price:Optional[int] = Field(None, gt=0)
    category:Optional[str] = None


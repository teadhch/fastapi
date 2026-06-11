# 파일 위치 : fastapi_basic/app/schemas/image_llm.py
# 역할 : LLM API의 입출력 데이터 구조(json)만 정의합니다.
#       (실제 LLM API의 호출 코드는 이 파일에 없습니다)

from pydantic import BaseModel, Field

# LLM에게 이미지파일을 주고, 응답을 받아낼 용도
class ImageAnalysisResponse(BaseModel) :
    filename: str
    size_bytes: int
    description: str    # 이미지 전체 설명
    objects: list       # 탐지된 객체 목록
    mood: str           # 전반적인 분위기
    
# LLM에게 텍스트 파일을 주고, 응답을 받아낼 용도
class TextSummaryResponse(BaseModel) :
    filename: str
    original_length: int
    summary: str
    

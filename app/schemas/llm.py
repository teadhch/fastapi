# 파일 위치 : fastapi_basic/app/schemas/llm.py
# 역할 : LLM API의 입출력 데이터 구조(json)만 정의합니다.
#      (실제 llm API의 호출 코드는 이 파일에 없습니다)

from pydantic import BaseModel, Field

# LLM에게 텍스트를 주고, 텍스트를 요약 요청할때 사용
class SummarizeRequest(BaseModel) :
    text:str = Field(..., min_length=10, description="요약할 텍스트")
    max_length:int = Field(100, ge=10, le=500, description="요약 최대 길이(글자의)", deprecated="다음 버전에서 없어질 가능성이 있습니다. replace=....")
    language:str = Field("ko", description="출력 언어(ko/en/jp)")

    # 예시 (Swagger UI documents에 보여질 내용)
    model_config = {
        "json_schema_extra" : {
            "example": {
                "text" : "FastAPI는 파이썬의 기반의...",
                "max_length" : 50,
                "language" : "en"
            }
        }
    }

# LLM이 요약한 응답을 받을 때 사용
class SummarizeResponse(BaseModel) :
    original_length : int # 원본 텍스트의 길이
    summary : str # LLM이 생성한 요약문

# LLM에게 리뷰를 보내고 긍정/부정인지 평가를 원한다면...
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="감정 분석할 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {"text": "이 책은 정말 훌륭하고 내용이 알차네요!"}
        }
    }

# LLM이 응답한 리뷰 감정 분석 결과용
class SentimentResponse(BaseModel):
    text:      str    # 입력 텍스트
    sentiment: str    # "긍정" | "부정" | "중립"
    score:     float  # 0.0 ~ 1.0
    reason:    str    # 판단 근거
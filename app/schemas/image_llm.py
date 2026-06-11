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

class ImageAnalysisForm:
    """
    이미지 분석 엔드포인트의 Form 파라미터를 하나로 묶은 클래스.
    Depends()로 라우터에 주입됩니다.
    """
    def __init__(
        self,
        prompt: str = Form(
            "이미지를 자세히 설명하고, 보이는 객체와 전반적인 분위기를 알려주세요.",
            description="분석 지시"
        ),
        language: str = Form(
            "ko",
            description="출력 언어 (ko/en)"
        ),
    ):
        self.prompt   = prompt
        self.language = language

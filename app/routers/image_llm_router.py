# 파일 위치: fastapi_basic/app/routers/image_llm_router.py
# 역할 : HTTP 요청(크라이언트가 보낸 REQUEST(클라이언트가 보낸 모든 요청정보(데이터 포함)))을 받아, Service단을 호출하고, 
#       Client에게 응답을 반환한다.


from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import json

from app.schemas.image_llm import *
from app.services.file_analyze_service import validate_image
image_llm_router = APIRouter(prefix="/imagellm", tags=["LLM"])

# Form 파라미터 클래스
# 이미지 분석의 엔드포인트의 Form 파라미터를 하나로 묶은 클래스
# Depends()로 라우터에 주입한다


# "/imagellm/analyze_image"
# 파일 + 텍스트 함께 받기
# JSON Body와 File은 함께 쓸수가 없다
# Form : 나머지 텍스트 데이터를 받는.. (form 태그의 데이터)
@image_llm_router.post(
    "/analyze_image",
    response_model= ImageAnalysisResponse,
    status_code = 201,
    tags=["LLM 이미지분석"],
    summary="이미지 설명 생성(Vision Model API 이용)"
)
async def analyze_image(
    # Form파라미터를 라우터에 직접 작성 - 파라미터가 많으면 시그니처가 길어져서 코드가 지저분해짐
    file:UploadFile = File(...),    # 이미지 파일
    form: ImageAnalysisForm = Depends(),    # 나머지 텍스트 데이터
    ) :
    """
    이미지를 업로드하면 GPT-4o Vision이 설명을 생성합니다.

    Form 파라미터:
    - `prompt`  : 분석 지시 (기본값 제공)
    - `language`: 출력 언어 ko/en
    """
    contents = await file.read()    # 파일 읽기
    validate_image(file.content_type, len(contents)) # 검증

    

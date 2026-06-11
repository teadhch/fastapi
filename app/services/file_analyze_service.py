# =====================================================
# 파일 위치: app/services/file_analyze_service.py
# =====================================================
# 이미지파일 형식인지 아닌지 검증

import base64, asyncio, json
from fastapi import HTTPException

from app.services.llm_service import get_llm_client, _call_with_timeout
MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10MB
MAX_TEXT_SIZE = 1 * 1024 * 1024     # 1MB 

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg"}
ALLOWED_TEXT_TYPES  = {"text/plain", "application/octet-stream"}

LANG_MAP = {"ko": "한국어", "en": "English"}

def validate_image(content_type:str, size:int) :
    """
    이미지 형식·크기를 검증합니다.
    실패 시 HTTPException을 발생시킵니다.
    Router가 아닌 Service에 검증 로직을 두면
    여러 엔드포인트에서 재사용할 수 있습니다.
    """
    if content_type not in ALLOWED_IMAGE_TYPES :
        raise HTTPException(
            status_code = 413,
            detail = "JPG/PNG만 허용됩니다. 받은형식 : {content_type}"
        )
    if size < 0 or size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"이미지 사이즈가 0이거나, 이미지 사이즈가 오버됩니다. ( 10MB. ) 현재: {size:,} bytes"
        )

async def analyze_image_with_llm(
        contents:bytes,
        prompt:str,
        language:str
) -> dict :
    """
    이미지를 Base64로 인코딩해 Vision API에 전달합니다.
    {"description": ..., "objects": [...], "mood": ...} 반환
    """
    client = get_llm_client()
    lang = LANG_MAP.get(language, "한국어")
    b64 = base64.b64encode(contents).decode("UTF-8")
    
    full_prompt = (
        f"{prompt}\n"
        f"반드시 {lang}로 출력하세요.\n"
        '아래 JSON 형식으로만 반환하세요:\n'
        '{"description":"...","objects":["..."],"mood":"..."}'
    )

    async def _call() :
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                },
                {"type": "text", "text": full_prompt},
            ]}],
            response_format={"type": "json_object"},
            max_tokens=500,
        )
        return response.choices[0].message.content
    
    

    try:
        raw = await _call_with_timeout(coro=_call(), timeout=60)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise HTTPException(502, detail="JSON 파싱 실패")

async def summarize_text_with_llm(
    text:       str,
    max_length: int,
    language:   str,
) -> str:
    """텍스트를 GPT-4o로 요약합니다. 요약 문자열을 반환합니다."""
    client = get_llm_client()
    lang   = LANG_MAP.get(language, "한국어")

    async def _call():
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"텍스트를 {max_length}자 이내로 핵심만 요약하세요. "
                        f"반드시 {lang}로 출력하세요."
                    )
                },
                {"role": "user", "content": text},
            ],
            max_tokens=400,
            temperature=0.3,
        )
        return response.choices[0].message.content

    try:
        return await _call_with_timeout(_call(), timeout=30.0)
    except asyncio.TimeoutError:
        raise HTTPException(503, detail="LLM 응답 시간 초과")
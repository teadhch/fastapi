# =====================================================
# 파일 위치: app/services/file_analyze_service.py
# =====================================================
# 이미지파일 형식인지 아닌지 검증

import base64, asyncio, json
from fastapi import HTTPException

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
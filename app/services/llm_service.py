# 파일 위치: fastAPI_basic\app\services\llm_service.py

# 역할 : 실제 LLM API의 호출 로직 담당
        # (HTTP 요청/응답 처리는 여기 음따)

import asyncio, json
from fastapi import HTTPException

LLM_TIMEOUT = 30.0      # LLM 호출 대기시간 (초)

def get_llm_client() :
    """
    OpenAI 클라이언트를 호출 시점에 생성합니다.

    모듈 상단에서 바로 AsyncOpenAI()를 생성하면
    import 시점에 OPENAI_API_KEY를 읽으려 해서
    load_dotenv() 호출 전에 오류가 발생합니다.

    이 함수를 통해 호출 시점에 생성하면
    load_dotenv()가 먼저 실행된 후 키를 읽으므로 안전합니다.
    """

    from openai import AsyncOpenAI
    return AsyncOpenAI()

async def _call_with_timeout(coro, timeout:float = LLM_TIMEOUT) :
    "_로 시작하는 함수는 내부에서 실행하는"
    """
    LLM 호출에 타임아웃을 적용하는 내부 헬퍼.
    timeout 초 안에 응답이 없으면 503을 반환합니다.
    """
    try : 
        # coro 를 호출하여 timeout 동안 응답을 기다린다.
        # await 때문에 다른 작업을 비동기로 수행 하며 기다림.
        # timeout동안 응답이 없으면 asyncio. TimeoutError 예외 발생
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail=f"LLM 응답 시간 초과 ({timeout} 처). 잠시 후에 다시 시도하세요..."
        )
    
async def summarize(text:str, max_length:int, language:str) -> str:
    """
    텍스트를 GPT-4o로 요약합니다.
    요약 결과 문자열을 반환합니다.
    """
    client = get_llm_client()
    lang_str = "한국어" if language =="ko" else "English"

    async def _call() :
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"텍스트를 {max_length}자 이내로 핵심만 요약하세요. "
                        f"출력 언어: {lang_str}"
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.3,
        )
        return response.choices[0].message.content
    
    return await _call_with_timeout(coro=_call())

async def analyze_sentiment(text:str) -> dict :
    """
    텍스트의 감정을 분석합니다.
    {"sentiment": "긍정|부정|중립", "score": 0.0~1.0, "reason": "..."} 반환
    """
    client = get_llm_client()

    async def _call():
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        '감정을 분석해서 아래 JSON 형식으로만 반환하세요.\n'
                        '{"sentiment":"긍정|부정|중립","score":0.0~1.0,"reason":"판단근거"}'
                    )
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"},   # JSON 응답 강제
            max_tokens=150,
            temperature=0,
        )
        return response.choices[0].message.content

    raw = await _call_with_timeout(_call())

    try :
        return json.load(raw)
    except json.JSONDecodeError :
        raise HTTPException(status_code=502, detail="JSON파싱실패")
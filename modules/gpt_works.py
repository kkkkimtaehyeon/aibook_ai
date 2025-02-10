import os
import json
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# 환경 변수 로드
_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI 클라이언트 생성
CLIENT = OpenAI(api_key=OPENAI_API_KEY)


def generate_story(messages):
    """GPT-4o-mini를 사용하여 동화의 다음 문장 3가지 옵션 생성"""
    response = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        response_format={"type": "json_object"},
        messages=messages
    )

    # JSON 응답 파싱
    return json.loads(response.choices[0].message.content)


def generate_base_story_prompt(source: str):
    """ 동화의 첫 페이지를 생성하는 프롬프트 """
    return [
        {"role": "system", "content": "너는 아이를 위한 동화를 작성하는 조수야."},
        {"role": "user", "content": f'''사용자의 이야기: ```{source}```
        이걸 기반으로 동화 첫 페이지의 시작이 될 3가지 버전의 문장을 작성해.
        반드시 다음 JSON 형식으로 답변해:

        {{
            "contentOption1": "첫 번째 문장 후보",
            "contentOption2": "두 번째 문장 후보",
            "contentOption3": "세 번째 문장 후보"
        }}
        '''}
    ]


def generate_story_prompt(source: str, page_number: int):
    """동화의 특정 페이지를 생성하는 프롬프트"""
    return [
        {"role": "system", "content": f"""
            너는 어린 아이를 위한 동화를 작성하는 조수야. 
            사용자가 매 페이지에서 서로 다른 선택지를 고르며 이야기를 만들어가는 구조야.
            1페이지부터 10페이지까지 발단, 전개, 절정, 결말을 가지는 이야기를 만들어야 해.
            지금은 {page_number} 페이지야. 이전 내용을 기반으로 다음 문장을 3가지 버전으로 만들어줘.
            사용자가 각각 다른 선택을 하면 이야기가 다르게 전개될 수 있도록 흐름을 다르게 작성해야 해.
        """},
        {"role": "user", "content": f'''이전 내용: ```{source}```  
        이 내용을 기반으로 다음 페이지의 첫 문장을 3가지 버전으로 생성해줘.  
        반드시 다음 JSON 형식으로 답변해:

        {{
            "contentOption1": "첫 번째 문장 후보",
            "contentOption2": "두 번째 문장 후보",
            "contentOption3": "세 번째 문장 후보"
        }}
        '''}
    ]


# # 예제 실행
# story_so_far = "옛날 옛날에 한 마을에 작은 토끼가 살고 있었어요."
# page_number = 1  # 현재 페이지 번호
# messages = generate_story_prompt(story_so_far, page_number)
#
# # 동화 생성 실행
# result = generate_story(messages)
# print(result)

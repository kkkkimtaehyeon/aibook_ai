import json

from fastapi import APIRouter
from pydantic import BaseModel, Field

from config.redis_config import redis_client
from service.StoryGenerationServiceV2 import TempStory

router = APIRouter()

redis = redis_client


@router.get("/health/redis")
async def redis_health():
    try:
        pong = await redis.ping()
        if pong:
            return {"status": "ok"}
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }


base_story = """
놀이터 옆 화단에서 애벌레를 봤어요.
초록색이고 통통했어요.
느릿느릿 기어가고 있었어요.
처음에는 무서웠어요.
근데 가만히 보니까 귀여웠어요.
손가락으로 살짝 건드려봤어요.
꿈틀꿈틀 움직였어요.
친구한테도 보여줬어요.
잎사귀 위에 올려주고 인사했어요.
“나비 돼서 다시 와~!”
"""
contents = [
    "오늘도 나는 놀이터로 갔어요. 그런데, 놀이터 옆 화단에서 뭔가 꿈틀거렸어요. 초록색 작은 애벌레였어요!",
    "“으악! 저게 뭐야!” 처음엔 깜짝 놀랐어요. 조금 무서웠어요. 그런데 가만히 보니까, 애벌레가 통통하고 귀엽게 생겼어요.",
    "애벌레는 느릿느릿 기어가고 있었어요. 작은 다리로 땅을 톡톡톡 기었어요. 정말 열심히 움직이고 있었어요.",
    "나는 조심조심 손가락으로 애벌레를 살짝 건드려봤어요. 애벌레는 깜짝 놀라더니 꿈틀꿈틀 움직였어요.",
    "“앗, 미안해! 놀랐지?” 나는 애벌레에게 말을 걸었어요. 애벌레는 말은 안 했지만, 가만히 내 손가락을 쳐다봤어요.",
    "“이름이 뭐야? 그냥… 꿈틀이라고 부를게!” 나는 애벌레에게 이름을 지어줬어요. 꿈틀이는 작은 잎 위로 올라갔어요. 초록색 몸이 반짝반짝 빛났어요.",
    "나는 친구를 불러서 꿈틀이를 보여줬어요. “우와, 애벌레다! 귀엽다!” 친구도 꿈틀이를 좋아했어요. 다 같이 잎사귀를 따서 꿈틀이를 조심히 옮겼어요.",
    "“꿈틀아, 너 나중에 나비 될 거지?” 나는 작은 목소리로 말했어요. “그럼 나비가 되면 꼭 다시 와!” 꿈틀이는 나뭇잎 위에서 천천히 몸을 말았어요.",
    "며칠이 지났어요. 그날의 꿈틀이를 잊지 않았어요. 그리고 오늘! 놀이터 화단 위에서 아름다운 나비 한 마리를 봤어요.",
    "“혹시… 꿈틀이니?” 나비는 내 앞을 한 바퀴 날더니 하늘 높이 날아올랐어요. 나는 소리쳤어요. “잘 가, 꿈틀아! 또 보자!”"
]


class TestRequest(BaseModel):
    base_story: str = Field(..., alias="baseStory"),
    contents: list[str] = Field(..., alias="contents")


@router.post("/redis/set")
async def set():
    story_dict = {
        "base_story": base_story,
        "contents": contents
    }
    await redis.set("testkey", json.dumps(story_dict))
    return {
        "status": "ok"
    }


@router.get("/redis/get")
async def get():
    raw_json = await redis.get("testkey")
    json_dict = json.loads(raw_json)
    story = TempStory.from_dict(json_dict)
    return {
        "baseStory": story.base_story,
        "contents": story.contents
    }

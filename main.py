from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import story_router, voice_cloning_router, image_generation_router, health_router

# from api import story_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],  # 프론트 서버, API 서버
    allow_credentials=True,
    allow_methods=["POST"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(story_router.router)
app.include_router(voice_cloning_router.router)
app.include_router(image_generation_router.router)
app.include_router(health_router.router)

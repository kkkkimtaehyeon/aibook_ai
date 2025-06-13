import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import story_generation_router, voice_cloning_router, image_generation_router, health_router
app = FastAPI()

_ = load_dotenv()
FRONT_DEPLOY_SERVER = os.getenv('front-domain')
FRONT_LOCAL_SERVER = "http://localhost:5174"
BACK_LOCAL_SERVER = "http://localhost:8080"

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # 프론트 서버, API 서버
    allow_origins=[FRONT_DEPLOY_SERVER, FRONT_LOCAL_SERVER, BACK_LOCAL_SERVER],  # 프론트 서버, API 서버
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(story_generation_router.router)
app.include_router(voice_cloning_router.router)
app.include_router(image_generation_router.router)
app.include_router(health_router.router)

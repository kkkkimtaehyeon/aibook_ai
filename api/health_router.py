from fastapi import APIRouter

router = APIRouter()


@router.get("/ai/health")
async def health():
    return "health"

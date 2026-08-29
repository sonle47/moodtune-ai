from fastapi import APIRouter

from models.schemas import VideoResponse
from services.youtube import find_video_id

router = APIRouter()


@router.get("/api/video", response_model=VideoResponse)
def get_video(title: str, artist: str):
    return {"video_id": find_video_id(title, artist)}

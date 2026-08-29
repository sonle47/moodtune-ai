from fastapi import APIRouter

from models.schemas import MoodRequest, MoodResponse
from services.gemini_client import generate_content, strip_result
from services.search import add_search_links

router = APIRouter()


@router.post("/api/mood", response_model=MoodResponse)
def get_playlist(request: MoodRequest):
    data = strip_result(generate_content(mood=request.mood_text))
    data["playlist"] = add_search_links(data["playlist"])
    return data

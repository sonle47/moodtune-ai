from pydantic import BaseModel

class MoodRequest(BaseModel):
    mood_text: str

class Track(BaseModel):
    title: str
    artist: str
    reason: str
    search_url: str


class MoodResponse(BaseModel):
    interpreted_mood: str
    message: str
    playlist: list[Track]


class VideoResponse(BaseModel):
    video_id: str | None
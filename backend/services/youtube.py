import os

import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def find_video_id(title, artist):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "q": f"{title} {artist}",
            "type": "video",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY,
        },
        timeout=10,
    )
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[0]["id"]["videoId"] if items else None

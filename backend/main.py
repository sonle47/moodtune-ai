import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from controllers.playlist import router as playlist_router
from controllers.videos import router as videos_router


app = FastAPI(title="MoodTune AI")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlist_router)
app.include_router(videos_router)


@app.get("/")
def health_check():
    return {"message": "Welcome to the MoodTune AI"}


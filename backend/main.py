import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from controllers.moods import router as moods_router
from controllers.videos import router as videos_router


app = FastAPI(title="MoodTune AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(moods_router)
app.include_router(videos_router)


@app.get("/")
def health_check():
    return {"message": "Welcome to the MoodTune AI"}


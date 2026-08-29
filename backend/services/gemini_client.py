import json
import os

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """A student just told you how they feel: "{mood}"

Reply with ONLY valid JSON (no markdown, no extra text) in exactly this shape:
{{
  "interpreted_mood": "a few words describing what they actually need",
  "message": "one short, warm sentence to the student explaining the pick",
  "playlist": [
    {{"title": "song title", "artist": "artist name", "reason": "why it fits, 5-8 words"}}
  ]
}}

Suggest exactly 10 real, well-known songs that fit the mood."""

def generate_content(mood):
    prompt = PROMPT_TEMPLATE.format(mood=mood)
    
    result = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return result

def strip_result(result):
    text = result.text.strip().removeprefix("```json").removesuffix("```").strip()
    data = json.loads(text)
    return data
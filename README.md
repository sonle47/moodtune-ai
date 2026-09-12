# MoodTune AI
- Frontend: https://moodtune-ai-blue.vercel.app
- Backend: https://moodtune-ai-5aaj.onrender.com/docs

> [!NOTE]
> Both run on free tiers. Render's free tier puts the backend to sleep
> after 15 minutes with no traffic, so if the site looks stuck loading the
> first time, which is just waking back up (30-50 seconds).
> Every request after that first one is fast again.

It's 11pm, I have an exam in the
morning, and I've just spent twenty minutes scrolling playlists instead of
studying. So I decided to build the moodTune AI app to it how
I'm feeling, and it hands me ten songs.

I'd never built anything that talks to an AI model before, past typing
into a chat box, as I wanted to find out what is actually going on underneath an
AI chat box like ChatGPT, Gemini, or Claude:

- How a prompt turns into a real API call
- How you get a language model to hand back something your code can use,
  instead of a paragraph of prose
- How a React app and a Python backend actually talk to each other

## What it does

- You type how you're feeling. Something like "stressed before an exam" or
  "need to lock in and study," basically whatever's actually true right now.
- Don't feel like typing? Just tap one of the mood suggession instead.
- That gets sent to Gemini, and it picks 10 real songs that match your mood.
- Each song comes with a quick reason why it picked that one.
- Every song links to YouTube so you can just click and start listening.

## What I learned building it

This was my first time actually deploying an app for real, and my first
time doing prompt engineering on purpose instead of just chatting with an AI. What has challenged me:

- This was also the first time I actually learned how to use git for
  real commits, pushing, branches, all of it, not just local project on computer.
- Working with Claude Code taught me how to actually structure debugging and learning step by step, instead of just guessing at random until something worked.
- Getting an LLM to reply with clean JSON instead of a paragraph is its own
  It's much more effective to show the model the exact shape you desire.
  Just explaining it in words.
- Even then, Gemini kept wrapping its JSON in markdown code fences, like it
  I was preparing a chat reply rather than sending the raw data, which caused json.loads() to fail until cutting that wrapper away so only the raw `{...}`
- React state finally clicked once I stopped thinking "the UI" and started
  thinking about what changes in the data and what occurs when it does.
- At first CORS was confusing, but it turned out that the browser was just blocking it.
  your frontend and backend from talking since they run on different
  Ports and by adding the CORS middleware on the backend the problem is solved.
- FastAPI gives you a free Swagger page for every endpoint, so I could
  check the backend by itself and in no way interact with the frontend.
- Building it stage by stage (health check, then models, then the AI call,
  After the prompt and then the frontend, it was much easier to track down bugs.
- Deploying it taught me the backend (Render) and frontend (Vite, on
  In order for Vercel to connect with each other they need to know each other's real URLs.
- I only found out why API keys can't just sit in a regular file after
  reading about real cases where leaked keys got abused and ran up huge
  bills for people. If it's not listed in `.gitignore`, it's basically
  public the second you push.

## Running it

1. Grab a free Gemini API key: https://aistudio.google.com/apikey
2. Backend:
   ```
   cd backend
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # paste your key in
   uvicorn main:app --reload --port 8000
   ```
3. Frontend, in a second terminal:
   ```
   cd frontend
   npm install
   npm run dev
   ```
4. Open http://localhost:5173

## How it fits together
<img width="1865" height="8192" alt="Untitled diagram-2026-09-12-224323" src="https://github.com/user-attachments/assets/e58d1c4a-ee48-4053-b6b4-238b1529396d" />

## What's next

I'm going to create a small text-to-mood classifier using scikit-learn, since Gemini currently handles all of that classification through an API call. My plan based on Claude Code:

- Write down several example phrases for each of my four moods (focus, chill, energize, destress)
- Convert those example phrases into numerical representations using a TfidfVectorizer
- Train a LogisticRegression model on those phrases so it can predict the mood associated with new text

This is a very basic form of supervised learning, however, it will be my own classification model from beginning-to-end, with no need for prompts or API keys. If this is successful, I would like to:

- Utilize this model to automatically highlight the corresponding mood chip while I am typing, prior to hitting "Tune in"
- Compare my classifier results with those of Gemini on a set of common test phrases, to identify areas where the two provide differing classifications

# AI Interview Agent — Backend

FastAPI backend implementing the ABTalks Problem Statement 2 contract.

## Required endpoint

`POST /api/interview`

First request:
```json
{
  "sessionId": "abc-123",
  "candidate": { "...candidate.json object..." }
}
```

Later requests:
```json
{
  "sessionId": "abc-123",
  "message": "My answer..."
}
```

Final response:
```json
{
  "reply": "Thank you. That completes the technical interview.",
  "done": true,
  "feedback": {
    "summary": "...",
    "strengths": [],
    "gaps": [],
    "next": []
  }
}
```

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# or: cp .env.example .env

# Put your Gemini API key in .env
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000/api/interview`.

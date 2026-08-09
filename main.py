import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from google import genai
except Exception:
    genai = None

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

with open(DATA_DIR / "curriculum.json", "r", encoding="utf-8") as f:
    CURRICULUM = json.load(f)

with open(DATA_DIR / "candidates.json", "r", encoding="utf-8") as f:
    CANDIDATES = json.load(f)

DAY_MAP = {d["day"]: d for d in CURRICULUM["days"]}

# In-memory state is intentional: the hackathon explicitly says persistent accounts
# and long-term history are out of scope. The supplied sessionId maintains the
# conversation across requests.
SESSIONS: Dict[str, Dict[str, Any]] = {}

app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

QUESTION_LIMIT = 8


class InterviewRequest(BaseModel):
    sessionId: str = Field(min_length=1)
    candidate: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


def clean_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group(0))


def passed_missions(candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
    missions = candidate.get("missions", [])
    result = []
    for m in missions:
        if m.get("passed") is True:
            day = int(m["day"])
            if day in DAY_MAP:
                result.append({
                    "day": day,
                    "title": DAY_MAP[day]["title"],
                    "type": DAY_MAP[day]["type"],
                    "tools": DAY_MAP[day].get("tools", []),
                    "objectives": DAY_MAP[day].get("objectives", []),
                    "attempts": m.get("attempts", 1),
                })
    return result


def choose_topic_plan(candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
    passed = passed_missions(candidate)
    if not passed:
        raise ValueError("Candidate has no passed curriculum missions.")

    # Prefer technically rich days while still respecting the candidate's actual
    # completed missions. The ordering also creates broad curriculum coverage.
    preferred = [11, 10, 12, 13, 16, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 7, 8, 9, 18, 19, 26, 14, 15, 17, 3, 4, 5, 6, 1, 2]
    by_day = {x["day"]: x for x in passed}
    ordered = [by_day[d] for d in preferred if d in by_day]

    # Ensure at least four different days whenever the profile permits it.
    if len(ordered) < 4:
        ordered = passed[:]

    return ordered


def build_fallback_question(topic: Dict[str, Any], index: int, previous_answer: str = "") -> str:
    day = topic["day"]
    title = topic["title"]
    objective = topic["objectives"][index % len(topic["objectives"])]
    templates = [
        f"Let's start with {title}. Can you explain the core idea behind this topic and how you would apply it in a real AI system?",
        f"For Day {day}, one objective is to {objective.lower()}. Walk me through how you would approach that in practice.",
        f"Imagine you are designing a production system involving {title}. What engineering decision would you make first, and why?",
        f"You've completed {title}. What is one common mistake engineers make with this topic, and how would you avoid it?",
    ]
    return templates[index % len(templates)]


def gemini_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or genai is None:
        return None
    return genai.Client(api_key=key)


def generate_ai_turn(session: Dict[str, Any], candidate_answer: Optional[str], is_start: bool = False) -> Dict[str, Any]:
    client = gemini_client()
    topic = session["current_topic"]
    asked = session["asked_questions"]
    history = session["history"]

    completed_topics = [
        {"day": x["day"], "title": x["title"], "objectives": x["objectives"], "tools": x["tools"]}
        for x in session["topic_plan"]
    ]

    system = """
You are a senior AI engineering interviewer conducting a realistic technical interview.
This is NOT a quiz and NOT a fixed questionnaire.

Rules:
1. Interview only from curriculum topics the candidate has PASSED.
2. Ask one question at a time.
3. Maintain conversation context.
4. Use the candidate's previous answer to decide whether the next question should be
   a deeper follow-up, a clarification, a scenario question, or a new topic.
5. Prefer intelligent follow-ups when the answer contains a useful claim.
6. Cover at least 4 different curriculum days across the interview.
7. The interview must have at least 8 total questions. The backend will enforce the count.
8. Do not reveal hidden scoring criteria.
9. Be concise and professional. Do not use markdown tables.
10. Return JSON only.

Return exactly:
{
  "reply": "the next interviewer message/question",
  "topic_day": 12,
  "topic_title": "Prompt Engineering Fundamentals",
  "question_kind": "opening|follow_up|clarification|scenario|new_topic",
  "quality": "strong|mixed|weak|unknown",
  "notes": "brief internal evaluation note"
}
"""

    candidate_summary = {
        "member": candidate := session["candidate"]["member"],
        "passed_missions": completed_topics,
        "signals": session["candidate"].get("signals", {}),
    }

    history_text = "\n".join(
        f"{i+1}. Interviewer: {turn.get('question','')}\n   Candidate: {turn.get('answer','')}"
        for i, turn in enumerate(history[-8:])
    )

    prompt = f"""
Candidate profile:
{json.dumps(candidate_summary, indent=2)}

Current planned topic:
{json.dumps(topic, indent=2)}

Questions already asked: {len(asked)}
Distinct curriculum days already covered: {sorted(session["covered_days"])}

Recent conversation:
{history_text or "(none yet)"}

Latest candidate answer:
{candidate_answer or "(no answer yet; this is the opening question)"}

Generate the next interviewer turn.
"""

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=system + "\n" + prompt,
            config={"temperature": 0.55},
        )
        data = clean_json(response.text)
        if not data.get("reply"):
            raise ValueError("Empty AI reply")
        return data
    except Exception:
        # Graceful fallback keeps the demo usable even if the model is temporarily
        # unavailable. The app still follows the required session/API contract.
        return {
            "reply": build_fallback_question(topic, len(asked), candidate_answer or ""),
            "topic_day": topic["day"],
            "topic_title": topic["title"],
            "question_kind": "opening" if is_start else "new_topic",
            "quality": "unknown",
            "notes": "Fallback question generated because the LLM was unavailable.",
        }


def evaluate_answer(session: Dict[str, Any], answer: str) -> Dict[str, Any]:
    client = gemini_client()
    topic = session["current_topic"]

    if not client:
        words = len(answer.split())
        quality = "strong" if words >= 55 else "mixed" if words >= 20 else "weak"
        return {"quality": quality, "note": f"Answer length heuristic: {words} words."}

    prompt = f"""
You are evaluating one technical interview answer.
Topic: Day {topic["day"]} — {topic["title"]}
Objectives: {json.dumps(topic["objectives"])}
Candidate answer: {answer}

Return JSON only:
{{
  "quality": "strong|mixed|weak",
  "note": "one concise sentence explaining the technical quality"
}}
"""
    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={"temperature": 0.2},
        )
        return clean_json(response.text)
    except Exception:
        words = len(answer.split())
        return {"quality": "strong" if words >= 55 else "mixed" if words >= 20 else "weak",
                "note": "Fallback evaluation used."}


def choose_next_topic(session: Dict[str, Any]) -> Dict[str, Any]:
    # First cover unvisited days, then revisit a topic for deeper probing.
    for topic in session["topic_plan"]:
        if topic["day"] not in session["covered_days"]:
            return topic
    return session["topic_plan"][len(session["asked_questions"]) % len(session["topic_plan"])]


def build_feedback(session: Dict[str, Any]) -> Dict[str, Any]:
    evaluations = session["evaluations"]
    strong = sum(1 for e in evaluations if e["quality"] == "strong")
    weak = sum(1 for e in evaluations if e["quality"] == "weak")
    total = max(1, len(evaluations))
    score = round((strong * 100 + (total - strong - weak) * 72 + weak * 45) / total)

    strengths = []
    gaps = []

    topic_quality: Dict[int, List[str]] = {}
    for e in evaluations:
        topic_quality.setdefault(e["day"], []).append(e["quality"])

    for day, qualities in topic_quality.items():
        title = DAY_MAP.get(day, {}).get("title", f"Day {day}")
        if qualities.count("strong") >= max(1, len(qualities) // 2):
            strengths.append(f"Strong understanding demonstrated in {title}.")
        elif qualities.count("weak") >= max(1, len(qualities) // 2):
            gaps.append(f"Needs deeper understanding of {title}.")

    if not strengths:
        strengths.append("Shows willingness to reason through technical questions.")
    if not gaps:
        gaps.append("Continue practicing production-oriented explanations and trade-offs.")

    next_steps = [
        "Practice explaining one AI system end-to-end without relying on notes.",
        "For each weak topic, answer a why/how/trade-off question aloud.",
        "Use small architecture scenarios to improve technical communication.",
    ]

    covered = sorted(session["covered_days"])
    summary = (
        f"The candidate completed an {len(session['asked_questions'])}-question technical interview "
        f"covering curriculum days {', '.join(map(str, covered))}. "
        f"Overall performance was approximately {score}/100 based on answer quality and depth."
    )

    return {
        "summary": summary,
        "strengths": strengths[:4],
        "gaps": gaps[:4],
        "next": next_steps[:4],
        "score": score,
        "questions": len(session["asked_questions"]),
        "daysCovered": len(covered),
    }


def start_session(session_id: str, candidate: Dict[str, Any]) -> Dict[str, Any]:
    plan = choose_topic_plan(candidate)
    if len(plan) < 4:
        raise ValueError("Candidate profile does not contain enough curriculum coverage.")

    # Select the first topic and create the first question.
    session = {
        "session_id": session_id,
        "candidate": candidate,
        "topic_plan": plan,
        "current_topic": plan[0],
        "asked_questions": [],
        "history": [],
        "evaluations": [],
        "covered_days": set(),
    }
    ai = generate_ai_turn(session, None, is_start=True)
    question = ai["reply"]

    session["asked_questions"].append({
        "question": question,
        "day": session["current_topic"]["day"],
        "title": session["current_topic"]["title"],
        "kind": ai.get("question_kind", "opening"),
    })
    session["covered_days"].add(session["current_topic"]["day"])
    SESSIONS[session_id] = session

    return {
        "reply": "Welcome. Let's begin your interview.\n\n" + question,
        "done": False,
    }


@app.post("/api/interview")
def interview(req: InterviewRequest):
    sid = req.sessionId.strip()

    # First request: candidate is required.
    if sid not in SESSIONS:
        if not req.candidate:
            raise HTTPException(status_code=400, detail="candidate is required when starting a new session.")
        try:
            return start_session(sid, req.candidate)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    session = SESSIONS[sid]

    if session.get("completed"):
        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": session["feedback"],
        }

    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required for a conversation turn.")

    answer = req.message.strip()
    current_question = session["asked_questions"][-1]

    evaluation = evaluate_answer(session, answer)
    session["evaluations"].append({
        "day": current_question["day"],
        "quality": evaluation.get("quality", "mixed"),
        "note": evaluation.get("note", ""),
    })
    session["history"].append({
        "question": current_question["question"],
        "answer": answer,
        "day": current_question["day"],
    })

    # Finish after the candidate has answered question 8.
    if len(session["asked_questions"]) >= QUESTION_LIMIT:
        feedback = build_feedback(session)
        session["completed"] = True
        session["feedback"] = feedback
        return {
            "reply": "Thank you. That completes the technical interview.",
            "done": True,
            "feedback": feedback,
        }

    # Choose a new topic when we still need curriculum coverage; otherwise let the
    # LLM decide a follow-up on the current topic.
    if len(session["covered_days"]) < 4:
        session["current_topic"] = choose_next_topic(session)
        # Make the next topic different from the current one where possible.
        if session["current_topic"]["day"] == current_question["day"]:
            for t in session["topic_plan"]:
                if t["day"] != current_question["day"] and t["day"] not in session["covered_days"]:
                    session["current_topic"] = t
                    break
    else:
        # Alternate between new topic and deeper follow-up.
        if len(session["asked_questions"]) % 2 == 0:
            session["current_topic"] = choose_next_topic(session)
        else:
            session["current_topic"] = next(
                (t for t in session["topic_plan"] if t["day"] == current_question["day"]),
                session["current_topic"],
            )

    ai = generate_ai_turn(session, answer)
    question = ai["reply"]

    session["asked_questions"].append({
        "question": question,
        "day": session["current_topic"]["day"],
        "title": session["current_topic"]["title"],
        "kind": ai.get("question_kind", "follow_up"),
    })
    session["covered_days"].add(session["current_topic"]["day"])

    return {"reply": question, "done": False}

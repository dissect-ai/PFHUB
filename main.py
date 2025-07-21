### PFHub Backend System (FastAPI)

# ======================
# main.py
# ======================
from fastapi import FastAPI
from routers import users, matchmaking, debate, ai_judge, cases
from database.db import init_db

app = FastAPI(title="PFHub Backend API")

init_db()

# Register all routers
app.include_router(users.router, prefix="/users")
app.include_router(matchmaking.router, prefix="/matchmaking")
app.include_router(debate.router, prefix="/debate")
app.include_router(ai_judge.router, prefix="/ai-judge")
app.include_router(cases.router, prefix="/cases")

@app.get("/")
def root():
    return {"message": "PFHub API is live!"}

# Run with: uvicorn main:app --reload

# ======================
# models/user.py
# ======================
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    username: str
    email: str
    hashed_password: str
    elo: int = 1000
    role: str = "debater"

# ======================
# models/debate.py
# ======================
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Debate(BaseModel):
    id: Optional[str]
    pro_id: str
    con_id: str
    winner_id: Optional[str]
    topic: str
    transcript: List[str] = []
    judge_feedback: Optional[str] = ""
    created_at: datetime = datetime.utcnow()

# ======================
# models/case.py
# ======================
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Case(BaseModel):
    id: Optional[str]
    title: str
    author_id: str
    topic: str
    side: str  # "Pro" or "Con"
    content: str
    tags: List[str] = []
    visibility: str  # "public", "private", "team"
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None

# ======================
# services/elo.py
# ======================
def update_elo(winner_elo, loser_elo, k=32):
    expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    new_winner_elo = winner_elo + k * (1 - expected_win)
    new_loser_elo = loser_elo - k * expected_win
    return round(new_winner_elo), round(new_loser_elo)

# ======================
# services/judge.py
# ======================
def simple_ai_judge(transcript):
    pro_score = sum(1 for line in transcript if "Pro:" in line)
    con_score = sum(1 for line in transcript if "Con:" in line)
    winner = "Pro" if pro_score > con_score else "Con"
    feedback = f"Pro: {pro_score} vs Con: {con_score}. {winner} wins by volume."
    return winner, feedback

# ======================
# services/matchmaking.py
# ======================
queue = []  # Queue of (user_id, elo)


def add_to_queue(user_id, elo):
    queue.append((user_id, elo))


def find_match_for(user_id):
    for other in queue:
        if other[0] != user_id:
            opponent = other
            queue.remove(opponent)
            queue.remove((user_id, next(e for u, e in queue if u == user_id)))
            return opponent[0]
    return None

# ======================
# database/db.py
# ======================
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.pfhub

def init_db():
    print("MongoDB initialized")

# ======================
# routers/users.py
# ======================
from fastapi import APIRouter
from models.user import User

router = APIRouter()

users_db = []  # mock

@router.post("/register")
def register(user: User):
    users_db.append(user)
    return {"status": "registered", "user_id": len(users_db) - 1}

# ======================
# routers/matchmaking.py
# ======================
from fastapi import APIRouter
from services.matchmaking import add_to_queue, find_match_for

router = APIRouter()

@router.post("/queue")
def join_queue(user_id: str, elo: int):
    add_to_queue(user_id, elo)
    return {"message": f"{user_id} added to matchmaking queue."}

@router.get("/find")
def match(user_id: str):
    match_id = find_match_for(user_id)
    if match_id:
        return {"status": "match_found", "opponent": match_id}
    return {"status": "waiting"}

# ======================
# routers/debate.py
# ======================
from fastapi import APIRouter
from models.debate import Debate

router = APIRouter()

debates_db = []

@router.post("/start")
def start_debate(debate: Debate):
    debates_db.append(debate)
    return {"message": "Debate started", "debate_id": len(debates_db) - 1}

# ======================
# routers/ai_judge.py
# ======================
from fastapi import APIRouter
from services.judge import simple_ai_judge

router = APIRouter()

@router.post("/score")
def score(transcript: list):
    winner, feedback = simple_ai_judge(transcript)
    return {"winner": winner, "feedback": feedback}

# ======================
# routers/cases.py
# ======================
from fastapi import APIRouter
from models.case import Case

router = APIRouter()

cases_db = []

@router.post("/upload")
def upload_case(case: Case):
    cases_db.append(case)
    return {"message": "Case uploaded", "id": len(cases_db) - 1}

@router.get("/my-cases")
def list_cases():
    return cases_db

@router.get("/topic/{topic}")
def get_by_topic(topic: str):
    return [case for case in cases_db if case.topic == topic and case.visibility == "public"]

@router.get("/{id}")
def get_case(id: int):
    return cases_db[id] if 0 <= id < len(cases_db) else {"error": "Not found"}

@router.put("/{id}")
def update_case(id: int, updated_case: Case):
    if 0 <= id < len(cases_db):
        cases_db[id] = updated_case
        return {"message": "Case updated"}
    return {"error": "Not found"}

@router.delete("/{id}")
def delete_case(id: int):
    if 0 <= id < len(cases_db):
        del cases_db[id]
        return {"message": "Case deleted"}
    return {"error": "Not found"}

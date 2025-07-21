from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS: Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PFHub backend is alive"}

@app.get("/match")
def match():
    return {
        "match": "opponent_found",
        "elo_delta": 24,
        "note": "This is a fake matchmaking endpoint for now."
    }

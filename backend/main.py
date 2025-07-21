from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all frontend origins (temporary dev setup)
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
        "status": "match found",
        "opponent": "RandomDebater42",
        "elo_change": 24
    }

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn

from database import Base, engine, SessionLocal
from crud import create_user, get_user, update_coins
from schemas import UserCreate
from config import ENTRY_FEES
from game.room_manager import RoomManager
from game.match_manager import MatchManager

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI
app = FastAPI()

# Socket.IO
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Managers
room_manager = RoomManager()
match_manager = MatchManager()


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create user
@app.post("/create-user")
def create_new_user(data: UserCreate, db=Depends(get_db)):
    user = get_user(db, data.username)
    if user:
        return {"message": "User already exists", "user": user}

    return create_user(db, data)


# List rooms
@app.get("/")
def home():
    return {"message": "Ludo Server Running Successfully!"}


@app.get("/rooms")
def list_rooms():
    return ENTRY_FEES


# SOCKET.IO EVENTS
@sio.event
async def join_room(sid, data):
    user_id = data["user_id"]
    room_id = data["entry_fee"]

    if room_id not in room_manager.rooms:
        room_manager.create_room(room_id, room_id)

    room = room_manager.join_room(room_id, user_id)

    await sio.emit("room_update", room)

    if room["is_full"]:
        match_manager.start_match(room_id, room["players"], room["entry_fee"])
        await sio.emit("match_start", match_manager.matches[room_id])


@sio.event
async def match_winner(sid, data):
    room_id = data["room_id"]
    winner_id = data["winner_id"]

    match = match_manager.set_winner(room_id, winner_id)

    db = SessionLocal()
    winner = get_user(db, winner_id)
    new_coins = winner.coins + match["prize"]
    update_coins(db, winner_id, new_coins)

    await sio.emit("match_result", match)


# RUN SERVER
if __name__ == "__main__":
    uvicorn.run(socket_app, host="127.0.0.1", port=8000)

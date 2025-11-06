from fastapi import APIRouter, HTTPException
from core.models import Game
from room.models import Room
from .utils import create_group
from sqlmodel import Session
from scipy.stats import skewnorm, truncate
import random


router = APIRouter()

@router.post("/start{room_id}")
def start_game(session: Session, room_id: int):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    dist = skewnorm(a=-5, loc=12, scale=1)
    trunc = truncate(dist, 8, 15)
    trunc_dist = trunc.rvs(size=100)
    rounds = trunc_dist[random.randint(0, 100)]
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException()

    game = Game(max_rounds=int(rounds))

    session.add(Game)



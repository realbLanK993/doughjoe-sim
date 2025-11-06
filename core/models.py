from typing import override
from sqlmodel import Field, Relationship, SQLModel
import enum
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sibling_dir = os.path.join(parent_dir, 'room')
sys.path.append(sibling_dir)

from room.models import Room, User

class Game(SQLModel, table=True):
    id: int | None = Field(default=None,primary_key=True)
    room_id: int | None = Field(default=None, foreign_key="room.id")
    max_rounds: int | None = Field(default=12)
    current_round: int = Field(default=0)
    avg_fare: int = Field(default=4000)
    ob_penalty: int = Field(default=6000)
    ub_penalty: int = Field(default=3000)
    groups: list["Group"] = Relationship(back_populates="game")


class Sex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class AgeGroup(str, enum.Enum):
    infant = "0 - 1 yr old"
    toddler = "1 - 3 yrs old"
    pre_schoolers = "3 - 5 yrs old"
    children = "5 - 12 yrs old"
    teens = "13 - 19 yrs old"
    young_adults = "20 - 34 yrs old"
    adults = "35 - 54 yrs old"
    older_adults = "55 - 64 yrs old"
    senior = "65+ yrs old"

class Profession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    @override
    def __str__(self) -> str:
        return self.name


class Region(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    state: str
    country: str

    @override
    def __str__(self) -> str:
        return self.name

class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int | None = Field(default=None, foreign_key="")
    game: Game = Relationship(back_populates="game")
    people: list["Person"] = Relationship(back_populates="group")
    ticket_price: int = Field(default=4000)

class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sex: Sex | None
    age_group: AgeGroup | None
    profession_id: int | None = Field(default=None, foreign_key="team.id")
    profession: Profession | None = Relationship(back_populates="people")
    region_id: int | None = Field(default=None, foreign_key="region.id")
    region: Region | None = Relationship(back_populates="people")
    group_id: int | None = Field(default=None, foreign_key="group")
    group: Group | None = Relationship(back_populates="people")
    prob: float = Field(default=0.75)
    showed_up: bool = Field(default=False)



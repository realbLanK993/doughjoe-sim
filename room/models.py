from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    gamer_tag: int
    cookie: str = Field(index=True)
    room_id: int | None = Field(default=None, foreign_key="room.id")


class Room(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    users: list[User] = Relationship(back_populates="users")
    room_code: int






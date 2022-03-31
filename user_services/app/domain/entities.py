from pydantic import BaseModel


class Entity(BaseModel):
    """Base entity class"""
    id: str


class User(Entity):
    """The base user model"""
    name: str
    given_name: str
    family_name: str
    nickname: str
    email: str
    picture: str

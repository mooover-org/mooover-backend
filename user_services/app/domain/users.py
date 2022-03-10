from pydantic import BaseModel


class User(BaseModel):
    """The base user model"""
    user_id: int

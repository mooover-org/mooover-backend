from pydantic import BaseModel


class User(BaseModel):
    """The base user model"""
    user_id: int
    name: str
    # TODO(adipopbv): Add the needed fields to the user

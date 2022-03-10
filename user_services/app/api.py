import functools
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer

from domain.errors import NotFoundError
from domain.users import User
from repositories import MockUserRepository
from services import UserServices
from utils.validators import validate_jwt

router = APIRouter()
services = UserServices(MockUserRepository())


def require_auth(func) -> Any:
    """
    Decorator to check for authorization before giving access to resources.

    :param func: the function that needs to be decorated
    :return: the decorated function
    """

    @functools.wraps(func)
    def wrapper_require_auth(*args, **kwargs):
        validate_bearer_token(kwargs["bearer_token"])
        return func(*args, **kwargs)

    def validate_bearer_token(bearer_token) -> None:
        if not bearer_token:
            raise HTTPException(status_code=401, detail="User not authenticated")
        if bearer_token.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Authorization header must be "
                                                        "of type bearer")
        validate_jwt(bearer_token.credentials)

    return wrapper_require_auth


@router.get("/{user_id}/", response_model=User)
@require_auth
def get_user(user_id: int, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user by id.

    :param user_id: the id of the user as an integer
    :param bearer_token: the bearer token for authorization
    :return: the corresponding user
    :raises HTTPException: if user not found
    """
    try:
        user = services.get_user(user_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return user
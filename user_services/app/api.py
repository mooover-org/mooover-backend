import functools
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer

from app.domain.errors import NotFoundError, DuplicateError
from app.domain.users import User
from app.repositories import MockUserRepository
from app.services import UserServices
from app.utils.config import AppConfig
from app.utils.validators import JwtValidator

router = APIRouter()
services = UserServices(MockUserRepository())

jwt_validator = JwtValidator(AppConfig().auth0_config)


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
            raise HTTPException(
                status_code=401, detail="User not authenticated")
        if bearer_token.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Authorization header must be "
                                                        "of type bearer")
        jwt_validator.validate(bearer_token.credentials)

    return wrapper_require_auth


@router.get("/{user_id}", response_model=User)
@require_auth
async def get_user(user_id: int, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user by id.

    :param user_id: the id of the user as an integer
    :param bearer_token: the bearer token for authorization
    :return: the corresponding user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        user = services.get_user(user_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=User)
@require_auth
async def add_user(user: User, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a new user.

    :param user: the user to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added user
    :raises HTTPException: if authorization is invalid
    """
    try:
        # TODO(adipopbv): change pydantic implementation to something that works (
        #  like taking params from request body)
        user = services.add_user(user)
    except DuplicateError:
        raise HTTPException(status_code=409, detail="User already exists")
    return user

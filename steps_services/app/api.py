import functools
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer

from app.domain.errors import NotFoundError
from app.services import StepsServices
from app.utils.config import AppConfig
from app.utils.validators import JwtValidator

router = APIRouter()
services = StepsServices()

jwt_validator = JwtValidator(AppConfig().auth0_config)


def require_auth(func) -> Any:
    """
    Decorator to check for authorization before giving access to resources

    :param func: the function that needs to be decorated
    :return: the decorated function
    """

    @functools.wraps(func)
    async def wrapper_require_auth(*args, **kwargs):
        validate_bearer_token(kwargs["bearer_token"])
        return await func(*args, **kwargs)

    def validate_bearer_token(bearer_token) -> None:
        if not bearer_token:
            raise HTTPException(
                status_code=401, detail="User not authenticated")
        if bearer_token.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Authorization header must be "
                                                        "of type bearer")
        jwt_validator.validate(bearer_token.credentials)

    return wrapper_require_auth


@router.get("/ping", response_model=str)
async def ping():
    """
    Route for checking if the server is up

    :return: a string saying "pong"
    """
    return "pong"


@router.get("/auth", response_model=str, status_code=200)
@require_auth
async def auth(bearer_token=Depends(HTTPBearer())):
    """
    Route for checking if the user is authenticated

    :param bearer_token: the bearer token for authorization
    :return: a string saying "authenticated"
    :raises HTTPException: if authorization is invalid
    """
    return "authenticated"


@router.get("/{user_id}", status_code=200)
@require_auth
async def get_steps(user_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting the steps for a user

    :param user_id: the user's id
    :param bearer_token: the bearer token for authorization
    :return: the steps for the user
    :raises HTTPException: if authorization is invalid
    :raises NotFoundError: if the user is not found
    """
    try:
        return services.get_steps(user_id, bearer_token.credentials)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", status_code=200)
@require_auth
async def update_steps(user_id: str, steps: int, bearer_token=Depends(HTTPBearer())):
    """
    Route for updating the steps for a user

    :param user_id: the user's id
    :param steps: the steps to update
    :param bearer_token: the bearer token for authorization
    :return: the status of the operation
    :raises HTTPException: if authorization is invalid
    :raises NotFoundError: if the user is not found
    """
    try:
        services.update_steps(user_id, steps, bearer_token.credentials)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/add-to-steps/{user_id}", status_code=200)
@require_auth
async def add_to_steps(user_id: str, steps: int, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding to a user's current steps

    :param user_id: the user's id
    :param steps: the steps to add
    :param bearer_token: the bearer token for authorization
    :return: the status of the operation
    :raises HTTPException: if authorization is invalid
    :raises NotFoundError: if the user is not found
    """
    try:
        services.add_to_steps(user_id, steps, bearer_token.credentials)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/daily-goal/{user_id}", status_code=200)
@require_auth
async def get_daily_steps_goal(user_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting the daily steps goal for a user

    :param user_id: the user's id
    :param bearer_token: the bearer token for authorization
    :return: the daily steps goal for the user
    :raises HTTPException: if authorization is invalid
    :raises NotFoundError: if the user is not found
    """
    try:
        return services.get_daily_steps_goal(user_id, bearer_token.credentials)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/daily-goal/{user_id}", status_code=200)
@require_auth
async def update_daily_steps_goal(user_id: str, daily_steps_goal: int, bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a user's daily steps goal

    :param user_id: the user's id
    :param daily_steps_goal: the new daily steps goal
    :param bearer_token: the bearer token for authorization
    :return: the status of the operation
    :raises HTTPException: if authorization is invalid
    :raises NotFoundError: if the user is not found
    """
    try:
        services.update_daily_steps_goal(user_id, daily_steps_goal, bearer_token.credentials)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

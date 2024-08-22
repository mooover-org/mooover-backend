import functools
from typing import Any

from corelib.domain.errors import NotFoundError, DuplicateError, NoContentError
from corelib.utils.validators import JwtValidator
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse, Response

from app.config import AppConfig
from app.repositories import Neo4jUserRepository
from app.services import UserServices

router = APIRouter()

jwt_validator = JwtValidator(AppConfig().auth0_config)

user_repository = Neo4jUserRepository()
user_services = UserServices(user_repository)


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
            raise HTTPException(status_code=401, detail="User not authenticated")
        if bearer_token.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Authorization header must be "
                                                        "of type bearer")
        jwt_validator.validate(bearer_token.credentials)

    return wrapper_require_auth


@router.get("/ping", response_model=str, tags=["ping"])
async def ping():
    """
    Route for checking if the server is up

    :return: a string saying "pong"
    """
    return "pong"


@router.get("/{user_id}", status_code=200, tags=["user"])
@require_auth
async def get_user(user_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user by id

    :param user_id: the id of the user
    :param bearer_token: the bearer token for authorization
    :return: the corresponding user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        user = user_services.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return user.as_dict()


@router.get("", status_code=200, tags=["user"])
@require_auth
async def get_users(bearer_token=Depends(HTTPBearer())):
    """
    Route for getting all users

    :param bearer_token: the bearer token for authorization
    :return: a list of all users
    :raises HTTPException: if authorization is invalid
    """
    try:
        users = user_services.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return [user.as_dict() for user in users]


@router.post("", status_code=201, tags=["user"])
@require_auth
async def register_user(request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for registering a new user

    :param request: the request object containing the user to be registered
    :param bearer_token: the bearer token for authorization
    :return: status message
    :raises HTTPException: if authorization is invalid or user already exists or
    if user is not a valid user
    """
    try:
        json_data = await request.json()
        user_services.add_user(json_data["sub"], json_data["name"], json_data["given_name"], json_data["family_name"],
                               json_data["nickname"], json_data["email"], json_data["picture"], )
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "User added"}


@router.put("/{user_id}", status_code=200, tags=["user"])
@require_auth
async def update_user(user_id: str, request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a user

    :param user_id: the id of the user to be updated
    :param request: the request object containing the user to be updated
    :param bearer_token: the bearer token for authorization
    :return: status message
    :raises HTTPException: if user not found or authorization is invalid or if
    user is not a valid user
    """
    try:
        json_data = await request.json()
        user_services.update_user(json_data["sub"], json_data["name"], json_data["given_name"],
                                  json_data["family_name"], json_data["nickname"], json_data["email"],
                                  json_data["picture"], json_data["today_steps"], json_data["daily_steps_goal"],
                                  json_data["this_week_steps"], json_data["weekly_steps_goal"],
                                  json_data["app_theme"], )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "User updated"}


@router.get("/{user_id}/steps", status_code=200, tags=["user, steps"])
@require_auth
async def get_user_steps(user_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting the steps of a user

    :param user_id: the id of the user
    :param bearer_token: the bearer token for authorization
    :return: the steps of the user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        today_steps, this_week_steps = user_services.get_user_steps(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"today_steps": today_steps, "this_week_steps": this_week_steps}


@router.get("/{user_id}/group", status_code=204, tags=["user", "group"], response_class=Response)
@require_auth
async def get_group_of_user(user_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user's group

    :param user_id: the id of the user
    :param bearer_token: the bearer token for authorization
    :return: the corresponding group
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        group = user_services.get_group_of_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NoContentError as e:
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return JSONResponse(content=group.as_dict(), status_code=200)

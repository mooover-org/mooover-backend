import functools
from typing import Any

from corelib.domain.errors import NotFoundError
from corelib.utils.validators import JwtValidator
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer

from app.config import AppConfig
from app.repositories import Neo4jStepsRepository
from app.services import StepsServices

router = APIRouter()

jwt_validator = JwtValidator(AppConfig().auth0_config)

steps_repository = Neo4jStepsRepository()
steps_services = StepsServices(steps_repository)
steps_services.run_background_tasks()


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


@router.post("/{user_id}", status_code=200, tags=["steps, user, group"])
@require_auth
async def add_new_steps(user_id: str, request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding new steps to a user and possibly a group

    :param user_id: the id of the user to add steps to
    :param request: the request object containing the steps to be added
    :param bearer_token: the bearer token for authorization
    :return: status message
    :raises HTTPException: if authorization is invalid or if user not found
    """
    try:
        json_data = await request.json()
        steps = json_data["steps"]
        steps_services.add_new_steps(user_id, steps)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "Steps added"}

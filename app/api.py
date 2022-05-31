import functools
from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer

from app.domain.errors import NotFoundError, DuplicateError, NoContentError
from app.repositories import Neo4jUserRepository, Neo4jGroupRepository
from app.services import UserServices, GroupServices
from app.utils.config import AppConfig
from app.utils.validators import JwtValidator

router = APIRouter()
user_repository = Neo4jUserRepository()
group_repository = Neo4jGroupRepository()
user_services = UserServices(user_repository)
group_services = GroupServices(group_repository, user_repository)

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
            raise HTTPException(status_code=401,
                                detail="Authorization header must be "
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


@router.get("/auth", response_model=str, status_code=200, tags=["auth"])
@require_auth
async def auth(bearer_token=Depends(HTTPBearer())):
    """
    Route for checking if the user is authenticated

    :param bearer_token: the bearer token for authorization
    :return: a string saying "authenticated"
    :raises HTTPException: if authorization is invalid
    """
    return "authenticated"


@router.get("/users/{user_id}", status_code=200, tags=["user"])
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


@router.get("/users", status_code=200, tags=["user"])
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


@router.post("/users", status_code=201, tags=["user"])
@require_auth
async def add_user(request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a new user

    :param request: the request object containing the user to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added user
    :raises HTTPException: if authorization is invalid or user already exists or
    if user is not a valid user
    """
    try:
        json_data = await request.json()
        user_services.add_user(
            json_data["sub"],
            json_data["name"],
            json_data["given_name"],
            json_data["family_name"],
            json_data["nickname"],
            json_data["email"],
            json_data["picture"],
        )
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


@router.put("/users/{user_id}", status_code=200, tags=["user"])
@require_auth
async def update_user(user_id: str, request: Request,
                      bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a user

    :param user_id: the id of the user to be updated
    :param request: the request object containing the user to be updated
    :param bearer_token: the bearer token for authorization
    :return: the updated user
    :raises HTTPException: if user not found or authorization is invalid or if
    user is not a valid user
    """
    try:
        json_data = await request.json()
        user_services.update_user(
            json_data["sub"],
            json_data["name"],
            json_data["given_name"],
            json_data["family_name"],
            json_data["nickname"],
            json_data["email"],
            json_data["picture"],
            json_data["today_steps"],
            json_data["daily_steps_goal"],
            json_data["this_week_steps"],
            json_data["weekly_steps_goal"],
            json_data["app_theme"],
        )
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


@router.get("/users/{user_id}/group", status_code=200, tags=["user", "group"])
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
        raise HTTPException(status_code=204, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return group.as_dict()


@router.get("/groups/{group_id}", status_code=200, tags=["group"])
@require_auth
async def get_group(group_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a group by id

    :param group_id: the id of the group
    :param bearer_token: the bearer token for authorization
    :return: the corresponding group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        group = group_services.get_group(group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return group.as_dict()


@router.get("/groups", status_code=200, tags=["group"])
@require_auth
async def get_groups(nickname: str = "", bearer_token=Depends(HTTPBearer())):
    """
    Route for getting multiple groups

    :param nickname: the nickname of the group to filter by
    :param bearer_token: the bearer token for authorization
    :return: the corresponding groups
    :raises HTTPException: if authorization is invalid
    """
    try:
        groups = group_services.get_groups(nickname)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return [group.as_dict() for group in groups]


@router.post("/groups", status_code=201, tags=["group"])
@require_auth
async def add_group(request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a new group

    :param request: the request object containing the group to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added group
    :raises HTTPException: if authorization is invalid or if group already
    exists or if group is invalid or if the user already belongs to a group
    """
    try:
        json_data = await request.json()
        group_services.add_group(
            user_services.get_user(json_data["user_id"]),
            json_data["nickname"],
            json_data["name"],
        )
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "Group added"}


@router.put("/groups/{group_id}", status_code=200, tags=["group"])
@require_auth
async def update_group(group_id: str, request: Request,
                       bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a group

    :param group_id: the id of the group to be updated
    :param request: the request object containing the group to be updated
    :param bearer_token: the bearer token for authorization
    :return: the updated group
    :raises HTTPException: if group not found or authorization is invalid or if
    group is invalid
    """
    try:
        json_data = await request.json()
        group_services.update_group(
            json_data["nickname"],
            json_data["name"],
            json_data["today_steps"],
            json_data["daily_steps_goal"],
            json_data["this_week_steps"],
            json_data["weekly_steps_goal"]
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "Group updated"}


@router.delete("/groups/{group_id}", status_code=200, tags=["group"])
@require_auth
async def delete_group(group_id: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for deleting a group

    :param group_id: the id of the group to be deleted
    :param bearer_token: the bearer token for authorization
    :return: the deleted group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        group_services.delete_group(group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "Group deleted"}


@router.get("/groups/{group_id}/members", status_code=200, tags=["group, user"])
@require_auth
async def get_members_of_group(group_id: str,
                               bearer_token=Depends(HTTPBearer())):
    """
    Route for getting all members of a group

    :param group_id: the id of the group
    :param bearer_token: the bearer token for authorization
    :return: the members of the group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        members = group_services.get_members_of_group(group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return [member.as_dict() for member in members]


@router.put("/groups/{group_id}/members", status_code=200, tags=["group, "
                                                                 "user"])
@require_auth
async def add_member_to_group(group_id: str, request: Request,
                              bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a user to a group

    :param group_id: the id of the group to add the user to
    :param request: the request object containing the user to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added user
    :raises HTTPException: if authorization is invalid or if user already
    belongs to a group or if user is invalid
    """
    try:
        json_data = await request.json()
        group_services.add_member_to_group(
            json_data["user_id"],
            group_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
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


@router.delete("/groups/{group_id}/members/{user_id}", status_code=200,
               tags=["group, user"])
@require_auth
async def remove_member_from_group(user_id: str, group_id: str,
                                   bearer_token=Depends(HTTPBearer())):
    """
    Route for removing a user from a group

    :param user_id: the id of the user to remove
    :param group_id: the id of the group to remove the user from
    :param bearer_token: the bearer token for authorization
    :return: the removed user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        group_services.remove_member_from_group(user_id, group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: "
                                                    f"{str(e)}")
    return {"message": "User removed"}

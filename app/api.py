import functools
from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from py2neo.ogm import Repository as N4jDb

from app.domain.errors import NotFoundError, DuplicateError
from app.repositories import Neo4jUserRepository, Neo4jGroupRepository
from app.services import UserServices, GroupServices
from app.utils.config import AppConfig
from app.utils.validators import JwtValidator

router = APIRouter()
database = N4jDb(AppConfig().neo4j_config['HOST'],
                 user=AppConfig().neo4j_config['USER'],
                 password=AppConfig().neo4j_config['PASSWORD'])
user_repository = Neo4jUserRepository(database)
group_repository = Neo4jGroupRepository(database)
user_services = UserServices(user_repository)
group_services = GroupServices(group_repository)

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


@router.get("/user/{sub}", status_code=200)
@require_auth
async def get_user(sub: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user by id

    :param sub: the sub of the user
    :param bearer_token: the bearer token for authorization
    :return: the corresponding user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        user = user_services.get_user(sub)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()


@router.post("/user/", status_code=201)
@require_auth
async def add_user(request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a new user

    :param request: the request object containing the user to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added user
    :raises HTTPException: if authorization is invalid
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
    except DuplicateError:
        raise HTTPException(status_code=409, detail="User already exists")


@router.put("/user/{sub}", status_code=200)
@require_auth
async def update_user(sub: str, request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a user

    :param sub: the sub of the user to be updated
    :param request: the request object containing the user to be updated
    :param bearer_token: the bearer token for authorization
    :return: the updated user
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        json_data = await request.json()
        user_services.update_user(
            sub,
            json_data["name"],
            json_data["given_name"],
            json_data["family_name"],
            json_data["nickname"],
            json_data["email"],
            json_data["picture"],
            json_data["steps"],
            json_data["daily_steps_goal"],
            json_data["app_theme"],
        )
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/user/{sub}/group", status_code=200)
@require_auth
async def get_user_group(sub: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a user's group

    :param sub: the sub of the user
    :param bearer_token: the bearer token for authorization
    :return: the corresponding group
    :raises HTTPException: if user not found or authorization is invalid
    """
    try:
        group = user_services.get_user_group(sub)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return group.to_dict()


@router.get("/group/{nickname}", status_code=200)
@require_auth
async def get_group(nickname: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for getting a group by id

    :param nickname: the nickname of the group
    :param bearer_token: the bearer token for authorization
    :return: the corresponding group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        group = group_services.get_group(nickname)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.to_dict()


@router.post("/group/", status_code=201)
@require_auth
async def add_group(request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for adding a new group

    :param request: the request object containing the group to be added
    :param bearer_token: the bearer token for authorization
    :return: the newly added group
    :raises HTTPException: if authorization is invalid
    """
    try:
        json_data = await request.json()
        group_services.add_group(
            user_services.get_user(json_data["sub"]),
            json_data["name"],
            json_data["nickname"],
        )
    except DuplicateError:
        raise HTTPException(status_code=409, detail="Group already exists")


@router.put("/group/{nickname}", status_code=200)
@require_auth
async def update_group(nickname: str, request: Request, bearer_token=Depends(HTTPBearer())):
    """
    Route for updating a group

    :param nickname: the nickname of the group to be updated
    :param request: the request object containing the group to be updated
    :param bearer_token: the bearer token for authorization
    :return: the updated group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        json_data = await request.json()
        group_services.update_group(
            nickname,
            json_data["name"],
            json_data["steps"],
            json_data["daily_steps_goal"],
            json_data["weekly_steps_goal"]
        )
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Group not found")


@router.delete("/group/{nickname}", status_code=200)
@require_auth
async def delete_group(nickname: str, bearer_token=Depends(HTTPBearer())):
    """
    Route for deleting a group

    :param nickname: the nickname of the group to be deleted
    :param bearer_token: the bearer token for authorization
    :return: the deleted group
    :raises HTTPException: if group not found or authorization is invalid
    """
    try:
        group_services.delete_group(nickname)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Group not found")

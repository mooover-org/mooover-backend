import pytest

from domain.errors import NotFoundError
from repositories import MockUserRepository
from services import UserServices


def test_get_user():
    repo = MockUserRepository()
    services = UserServices(repo)
    assert services.get_user(1).user_id == 1
    with pytest.raises(NotFoundError):
        services.get_user(-1)

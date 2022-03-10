import pytest

from app.domain.errors import NotFoundError
from app.repositories import MockUserRepository


def test_find_one():
    repo = MockUserRepository()
    assert repo.find_one(1).user_id == 1
    with pytest.raises(NotFoundError):
        repo.find_one(-1)

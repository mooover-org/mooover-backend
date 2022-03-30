import pytest

from app.domain.errors import NotFoundError, DuplicateError
from app.repositories import Repository
from app.services import UserServices
from domain.entities import User


class TestUserServices:
    user1: User
    user2: User
    repo: Repository
    services: UserServices

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user1 = User(
            **{"id": "1", "name": "test", "given_name": "test",
               "family_name": "test", "nickname": "test", "email": "test@test.test",
               "picture": "test"})
        self.user2 = User(
            **{"id": "2", "name": "test", "given_name": "test",
               "family_name": "test", "nickname": "test", "email": "test@test.test",
               "picture": "test"})
        self.repo = Repository({self.user1.id: self.user1})
        self.services = UserServices(self.repo)

    def test_get_user(self):
        assert self.services.get_user(self.user1.id).id == self.user1.id
        with pytest.raises(NotFoundError):
            self.services.get_user(self.user2.id)

    def test_add_user(self):
        self.services.add_user(self.user2)
        assert self.services.get_user(self.user2.id).id == self.user2.id
        with pytest.raises(DuplicateError):
            self.services.add_user(self.user2)

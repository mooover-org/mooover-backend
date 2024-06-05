import pytest
from corelib.domain.errors import NotFoundError, DuplicateError
from corelib.domain.models import User
from corelib.repositories import Repository

from app.services import UserServices


class TestUserServices:
    user1: User
    user2: User
    repo: Repository
    services: UserServices

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user1 = User(sub='1', name='test', given_name='test', family_name='test', nickname='test',
                          email='test@test.test', picture='test')
        self.user2 = User(sub='2', name='test', given_name='test', family_name='test', nickname='test',
                          email='test@test.test', picture='test')
        self.repo = Repository({self.user1.id: self.user1})
        self.services = UserServices(self.repo)

    def test_get_user(self):
        assert self.services.get_user(self.user1.id).id == self.user1.id
        with pytest.raises(NotFoundError):
            self.services.get_user(self.user2.id)

    def test_add_user(self):
        self.services.add_user(self.user2.sub, self.user2.name, self.user2.given_name, self.user2.family_name,
                               self.user2.nickname, self.user2.email, self.user2.picture)
        assert self.services.get_user(self.user2.id).id == self.user2.id
        with pytest.raises(DuplicateError):
            self.services.add_user(self.user2.sub, self.user2.name, self.user2.given_name, self.user2.family_name,
                                   self.user2.nickname, self.user2.email, self.user2.picture)

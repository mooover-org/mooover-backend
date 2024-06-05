import pytest

from corelib.domain.errors import NotFoundError, DuplicateError
from corelib.repositories import Repository
from corelib.domain.models import Entity


class TestRepository:
    entity1: Entity
    entity2: Entity
    entity3: Entity
    repo: Repository

    @pytest.fixture(autouse=True)
    def setup(self):
        self.entity1 = Entity('1')
        self.entity2 = Entity('2')
        self.entity3 = Entity('3')
        self.repo = Repository({self.entity1.id: self.entity1})

    def test_get_one(self):
        assert self.repo.get_one(self.entity1.id).id == self.entity1.id
        with pytest.raises(NotFoundError):
            self.repo.get_one(self.entity2.id)

    def test_get_all(self):
        assert len(self.repo.get_all()) == 1
        assert self.repo.get_all()[0].id == self.entity1.id

    def test_add(self):
        assert len(self.repo.get_all()) == 1
        self.repo.add(self.entity2)
        assert len(self.repo.get_all()) == 2
        assert self.repo.get_one(self.entity2.id).id == self.entity2.id
        with pytest.raises(DuplicateError):
            self.repo.add(self.entity2)

    def test_update(self):
        assert len(self.repo.get_all()) == 1
        self.entity2.id = self.entity1.id
        self.repo.update(self.entity2)
        assert len(self.repo.get_all()) == 1
        assert self.repo.get_one(self.entity2.id).id == self.entity2.id
        with pytest.raises(NotFoundError):
            self.repo.update(self.entity3)

    def test_delete(self):
        assert len(self.repo.get_all()) == 1
        self.repo.delete(self.entity1.id)
        assert len(self.repo.get_all()) == 0
        with pytest.raises(NotFoundError):
            self.repo.delete(self.entity1.id)

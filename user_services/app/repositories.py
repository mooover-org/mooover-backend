from typing import Any

from py2neo.ogm import Repository as Neo4JRepository

from app.domain.errors import NotFoundError, DuplicateError
from app.domain.models import User
from app.utils.config import AppConfig


class Repository:
    """Abstract class for all repositories"""
    entities: dict = {}

    def __init__(self, entities=None) -> None:
        if entities:
            self.entities = entities

    def get_one(self, entity_id: str) -> Any:
        """
        Get one entity by id

        :param entity_id: The id of the entity
        :return: The entity
        """
        if entity_id not in self.entities:
            raise NotFoundError(entity_id)
        return self.entities[entity_id]

    def get_all(self) -> list:
        """
        Get all entities

        :return: A list of all entities
        """
        return [*self.entities.values()]

    def add(self, entity) -> None:
        """
        Add an entity to the repository

        :param entity: The entity to be added
        :return: None
        :raises: DuplicateError: If the entity already exists
        """
        if entity.id in self.entities:
            raise DuplicateError(entity.id)
        self.entities[entity.id] = entity

    def update(self, entity) -> None:
        """
        Update an entity in the repository

        :param entity: The entity to be updated
        :return: None
        :raises: NotFoundError: If the entity does not exist
        """
        if entity.id not in self.entities:
            raise NotFoundError(entity.id)
        self.entities[entity.id] = entity

    def delete(self, entity_id) -> None:
        """
        Delete an entity from the repository

        :param entity_id: The id of the entity to be deleted
        :return: None
        :raises: NotFoundError: If the entity does not exist
        """
        if entity_id not in self.entities:
            raise NotFoundError(entity_id)
        del self.entities[entity_id]

    def delete_all(self) -> None:
        """
        Delete all entities from the repository

        :return: None
        """
        self.entities = {}


class Neo4JUserRepository(Repository):
    """Neo4J repository for users"""

    entities: Neo4JRepository

    def __init__(self, host: str = AppConfig().neo4j_config['HOST'],
                 user: str = AppConfig().neo4j_config['USER'],
                 password: str = AppConfig().neo4j_config['PASSWORD']) -> None:
        super().__init__(Neo4JRepository(host, user=user, password=password))

    def get_one(self, entity_id: str) -> User:
        """
        Get one user by id

        :param entity_id: The id of the user
        :return: The user
        :raises: NotFoundError: If the user does not exist
        """
        user = self.entities.get(User, entity_id)
        if not user:
            raise NotFoundError(entity_id)
        return user

    def get_all(self) -> list:
        """
        Get all users

        :return: A list of all users
        """
        return self.entities.match(User)

    def add(self, entity: User) -> None:
        """
        Add a user to the repository

        :param entity: The user to be added
        :return: None
        :raises: DuplicateError: If the user already exists
        """
        user = self.entities.get(User, entity.id)
        if user and self.entities.exists(user):
            raise DuplicateError(entity.id)
        self.entities.save(entity)

    def update(self, entity: User) -> None:
        """
        Update a user in the repository

        :param entity: The user to be updated
        :return: None
        :raises: NotFoundError: If the user does not exist
        """
        self.get_one(entity.id)
        self.entities.save(entity)

    def delete(self, entity_id: str) -> None:
        """
        Delete a user from the repository

        :param entity_id: The id of the user to be deleted
        :return: None
        :raises: NotFoundError: If the user does not exist
        """
        user = self.entities.get(User, entity_id)
        self.entities.delete(user)

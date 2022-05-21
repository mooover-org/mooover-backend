from typing import Any

from py2neo.ogm import Repository as N4jDb

from app.domain.errors import NotFoundError, DuplicateError
from app.domain.models import User, Group
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


class Neo4jUserRepository(Repository):
    """Neo4J repository for users"""

    entities: N4jDb

    def __init__(self, database: N4jDb = N4jDb(AppConfig().neo4j_config['HOST'],
                                               user=AppConfig().neo4j_config['USER'],
                                               password=AppConfig().neo4j_config['PASSWORD'])) -> None:
        super().__init__(database)

    def get_one(self, user_id: str) -> User:
        """
        Get one user by id

        :param user_id: The id of the user
        :return: The user
        :raises: NotFoundError: If the user does not exist
        """
        user = self.entities.get(User, user_id)
        if not user:
            raise NotFoundError(user_id)
        return user

    def get_all(self) -> list:
        """
        Get all users

        :return: A list of all users
        """
        return self.entities.match(User)

    def add(self, user: User) -> None:
        """
        Add a user to the repository

        :param user: The user to be added
        :return: None
        :raises: DuplicateError: If the user already exists
        """
        user = self.entities.get(User, user.id)
        if user and self.entities.exists(user):
            raise DuplicateError(user.id)
        self.entities.save(user)

    def update(self, user: User) -> None:
        """
        Update a user in the repository

        :param user: The user to be updated
        :return: None
        :raises: NotFoundError: If the user does not exist
        """
        self.get_one(user.id)
        self.entities.save(user)

    def delete(self, user_id: str) -> None:
        """
        Delete a user from the repository

        :param user_id: The id of the user to be deleted
        :return: None
        :raises: NotFoundError: If the user does not exist
        """
        user = self.entities.get(User, user_id)
        self.entities.delete(user)


class Neo4jGroupRepository(Repository):
    """Neo4J repository for groups"""

    entities: N4jDb

    def __init__(self, database: N4jDb = N4jDb(AppConfig().neo4j_config['HOST'],
                                               group=AppConfig().neo4j_config['USER'],
                                               password=AppConfig().neo4j_config['PASSWORD'])) -> None:
        super().__init__(database)

    def get_one(self, group_id: str) -> Group:
        """
        Get one group by id

        :param group_id: The id of the group
        :return: The group
        :raises: NotFoundError: If the group does not exist
        """
        group = self.entities.get(Group, group_id)
        if not group:
            raise NotFoundError(group_id)
        return group

    def get_all(self) -> list:
        """
        Get all groups

        :return: A list of all groups
        """
        return self.entities.match(Group)

    def add(self, group: Group) -> None:
        """
        Add a group to the repository

        :param group: The group to be added
        :return: None
        :raises: DuplicateError: If the group already exists
        """
        group = self.entities.get(Group, group.id)
        if group and self.entities.exists(group):
            raise DuplicateError(group.id)
        self.entities.save(group)

    def update(self, group: Group) -> None:
        """
        Update a group in the repository

        :param group: The group to be updated
        :return: None
        :raises: NotFoundError: If the group does not exist
        """
        self.get_one(group.id)
        self.entities.save(group)

    def delete(self, group_id: str) -> None:
        """
        Delete a group from the repository

        :param group_id: The id of the group to be deleted
        :return: None
        :raises: NotFoundError: If the group does not exist
        """
        group = self.entities.get(Group, group_id)
        self.entities.delete(group)

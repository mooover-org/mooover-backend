from typing import Any

from app.domain.errors import NotFoundError, DuplicateError


class Repository:
    """Abstract class for all repositories"""
    entities = {}

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

    def add(self, entity) -> Any:
        """
        Add an entity to the repository

        :param entity: The entity to be added
        :return: The entity
        :raises: DuplicateError: If the entity already exists
        """
        if entity.id in self.entities:
            raise DuplicateError(entity.id)
        self.entities[entity.id] = entity
        return self.entities[entity.id]

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

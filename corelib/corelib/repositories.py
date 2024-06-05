from typing import Any, List

from corelib.domain.errors import NotFoundError, DuplicateError, InvalidContentError
from corelib.domain.models import Entity


class Repository:
    """Abstract class for all repositories"""

    entities: dict = {}

    def __init__(self, entities: dict) -> None:
        if type(entities) is not dict:
            raise InvalidContentError("repository contents have to be dict")
        self.entities = entities

    def get_one(self, entity_id: str) -> Any:
        """
        Get one entity by id

        :param entity_id: The id of the entity
        :return: The entity
        """
        if entity_id not in self.entities:
            raise NotFoundError("Entity not found")
        return self.entities[entity_id]

    def get_all(self) -> List[Any]:
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
        :raises DuplicateError: If the entity already exists
        """
        if entity.id in self.entities:
            raise DuplicateError("Entity already exists")
        self.entities[entity.id] = entity

    def update(self, entity) -> None:
        """
        Update an entity in the repository

        :param entity: The entity to be updated
        :return: None
        :raises NotFoundError: If the entity does not exist
        """
        if entity.id not in self.entities:
            raise NotFoundError("Entity not found")
        self.entities[entity.id] = entity

    def delete(self, entity_id: str) -> None:
        """
        Delete an entity from the repository

        :param entity_id: The id of the entity to be deleted
        :return: None
        :raises NotFoundError: If the entity does not exist
        """
        if entity_id not in self.entities:
            raise NotFoundError("Entity not found")
        del self.entities[entity_id]

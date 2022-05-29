from typing import Any, List

from neo4j import Neo4jDriver, GraphDatabase, Result

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

    def delete(self, entity_id) -> None:
        """
        Delete an entity from the repository

        :param entity_id: The id of the entity to be deleted
        :return: None
        :raises NotFoundError: If the entity does not exist
        """
        if entity_id not in self.entities:
            raise NotFoundError("Entity not found")
        del self.entities[entity_id]


class Neo4jUserRepository(Repository):
    """Neo4J repository for users"""

    driver: Neo4jDriver

    def __init__(self, driver: Neo4jDriver = GraphDatabase.driver(
        uri=AppConfig().neo4j_config['HOST'],
        auth=(AppConfig().neo4j_config['USER'],
              AppConfig().neo4j_config['PASSWORD']))) -> None:
        self.driver = driver
        super().__init__()

    def get_one(self, user_id: str) -> User:
        """
        Get one user by id

        :param user_id: The id of the user
        :return: The user
        :raises NotFoundError: If the user does not exist
        """

        def _get_user(tx, primary_key: str):
            result: Result = tx.run(
                f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                f"RETURN u "
                f"LIMIT 1"
            )
            record = result.single()
            if record:
                return User(**record.data()['u'])
            else:
                raise NotFoundError("User not found")

        with self.driver.session() as session:
            return session.read_transaction(_get_user, user_id)

    def get_all(self) -> List[User]:
        """
        Get all users

        :return: A list of all users
        """

        def _get_all_users(tx):
            result = tx.run(
                f"MATCH (u:User) "
                f"RETURN u"
            )
            return [User(**record.data()['u']) for record in result]

        with self.driver.session() as session:
            return session.read_transaction(_get_all_users)

    def add(self, user: User) -> None:
        """
        Add a user to the repository

        :param user: The user to be added
        :return: None
        :raises DuplicateError: If the user already exists
        """

        def _add_user(tx, user: User):
            tx.run(
                f"CREATE (u:User {user.as_str_dict()})",
            )

        try:
            self.get_one(getattr(user, User.__primarykey__))
            raise DuplicateError("User already exists")
        except NotFoundError:
            with self.driver.session() as session:
                session.write_transaction(_add_user, user)

    def update(self, user: User) -> None:
        """
        Update a user in the repository

        :param user: The user to be updated
        :return: None
        :raises NotFoundError: If the user does not exist
        """

        def _update_user(tx, user: User):
            tx.run(
                f"MATCH (u:User {{{User.__primarykey__}: "
                f"'{getattr(user, User.__primarykey__)}'}}) "
                f"SET u = {user.as_str_dict()}"
            )

        self.get_one(getattr(user, User.__primarykey__))
        with self.driver.session() as session:
            session.write_transaction(_update_user, user)

    def delete(self, user_id: str) -> None:
        """
        Delete a user from the repository

        :param user_id: The id of the user to be deleted
        :return: None
        :raises: NotFoundError: If the user does not exist
        """

        def _delete_user(tx, primary_key: str):
            tx.run(
                f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                f"DETACH DELETE u"
            )

        self.get_one(user_id)
        with self.driver.session() as session:
            session.write_transaction(_delete_user, user_id)

    def get_groups_of_user(self, user_id: str) -> List[Group]:
        """
        Get all the groups of a user

        :param user_id: The id of the user
        :return: A list of groups
        :raises NotFoundError: If the user does not exist
        """

        def _get_groups_of_user(tx, primary_key: str):
            result = tx.run(
                f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                f"-[:MEMBER_OF]->(g:Group) "
                f"RETURN g",
            )
            return [Group(**record.data()['g']) for record in result]

        self.get_one(user_id)
        with self.driver.session() as session:
            return session.read_transaction(_get_groups_of_user, user_id)


class Neo4jGroupRepository(Repository):
    """Neo4J repository for groups"""

    driver: Neo4jDriver

    def __init__(self, driver: Neo4jDriver = GraphDatabase.driver(
        uri=AppConfig().neo4j_config['HOST'],
        auth=(AppConfig().neo4j_config['USER'],
              AppConfig().neo4j_config['PASSWORD']))) -> None:
        self.driver = driver
        super().__init__()

    def get_one(self, group_id: str) -> Group:
        """
        Get one group by id

        :param group_id: The id of the group
        :return: The group
        :raises NotFoundError: If the group does not exist
        """

        def _get_group(tx, primary_key: str):
            result = tx.run(
                f"MATCH (g:Group {{{Group.__primarykey__}: '{primary_key}'}}) "
                f"RETURN g "
                f"LIMIT 1"
            )
            record = result.single()
            if record is not None:
                return Group(**record.data()['g'])
            else:
                raise NotFoundError("Group not found")

        with self.driver.session() as session:
            return session.read_transaction(_get_group, group_id)

    def get_all(self) -> List[Group]:
        """
        Get all groups

        :return: A list of all groups
        """

        def _get_all_groups(tx):
            result = tx.run(
                f"MATCH (g:Group) "
                f"RETURN g"
            )
            return [Group(**record.data()['g']) for record in result]

        with self.driver.session() as session:
            return session.read_transaction(_get_all_groups)

    def add(self, group: Group) -> None:
        """
        Add a group to the repository

        :param group: The group to be added
        :return: None
        :raises DuplicateError: If the group already exists
        """

        def _add_group(tx, group: Group):
            tx.run(
                f"CREATE (g:Group {group.as_str_dict()})"
            )

        try:
            self.get_one(getattr(group, Group.__primarykey__))
            raise DuplicateError("Group already exists")
        except NotFoundError:
            with self.driver.session() as session:
                session.write_transaction(_add_group, group)

    def update(self, group: Group) -> None:
        """
        Update a group in the repository

        :param group: The group to be updated
        :return: None
        :raises NotFoundError: If the group does not exist
        """

        def _update_group(tx, group: Group):
            tx.run(
                f"MATCH (g:Group {{{Group.__primarykey__}: "
                f"'{getattr(group, Group.__primarykey__)}'}}) "
                f"SET g = {group.as_str_dict()}"
            )

        self.get_one(getattr(group, Group.__primarykey__))
        with self.driver.session() as session:
            session.write_transaction(_update_group, group)

    def delete(self, group_id: str) -> None:
        """
        Delete a group from the repository

        :param group_id: The id of the group to be deleted
        :return: None
        :raises: NotFoundError: If the group does not exist
        """

        def _delete_group(tx, primary_key: str):
            tx.run(
                f"MATCH (g:Group {{{Group.__primarykey__}: '{primary_key}'}}) "
                f"DETACH DELETE g"
            )

        self.get_one(group_id)
        with self.driver.session() as session:
            session.write_transaction(_delete_group, group_id)

    def get_members_of_group(self, group_id: str) -> List[User]:
        """
        Get all members of a group

        :param group_id: The id of the group
        :return: A list of all members of the group
        :raises NotFoundError: If the group does not exist
        """

        def _get_members_of_group(tx, primary_key: str):
            result = tx.run(
                f"MATCH (u:User)-[:MEMBER_OF]->(g:Group "
                f"{{{Group.__primarykey__}: '{primary_key}'}}) "
                f"RETURN u"
            )
            return [User(**record.data()['u']) for record in result]

        self.get_one(group_id)
        with self.driver.session() as session:
            return session.read_transaction(_get_members_of_group, group_id)

    def add_member_to_group(self, user_id: str, group_id: str) -> None:
        """
        Add members to a group

        :param user_id: The id of the user to be added
        :param group_id: The id of the group to be added to
        :return: None
        :raises NotFoundError: If the user or group does not exist
        """

        def _add_member(tx, user_primary_key: str, group_primary_key: str):
            result = tx.run(
                f"MATCH (u:User {{{User.__primarykey__}: "
                f"'{user_primary_key}'}}) "
                f"RETURN u"
            )
            record = result.single()
            if record:
                tx.run(
                    f"MATCH (u:User {{{User.__primarykey__}: "
                    f"'{user_primary_key}'}}) "
                    f"MATCH (g:Group {{{Group.__primarykey__}: "
                    f"'{group_primary_key}'}}) "
                    f"CREATE (u)-[:MEMBER_OF]->(g)"
                )
            else:
                raise NotFoundError("User not found")

        self.get_one(group_id)
        with self.driver.session() as session:
            session.write_transaction(_add_member, user_id, group_id)

    def remove_member_from_group(self, user_id: str, group_id: str) -> None:
        """
        Remove members from a group

        :param user_id: The id of the user to be removed
        :param group_id: The id of the group to be removed from
        :return: None
        :raises NotFoundError: If the user or group does not exist
        """

        def _remove_member(tx, user_primary_key: str, group_primary_key: str):
            result = tx.run(
                f"MATCH (u:User {{{User.__primarykey__}:"
                f"'{user_primary_key}'}}) "
                f"RETURN u"
            )
            record = result.single()
            if record:
                tx.run(
                    f"MATCH (u:User {{{User.__primarykey__}: "
                    f"'{user_primary_key}'}}) "
                    f"MATCH (g:Group {{{Group.__primarykey__}: "
                    f"'{group_primary_key}'}}) "
                    f"MATCH (u)-[r:MEMBER_OF]->(g) "
                    f"DELETE r"
                )
            else:
                raise NotFoundError("User not found")

        self.get_one(group_id)
        with self.driver.session() as session:
            session.write_transaction(_remove_member, user_id, group_id)

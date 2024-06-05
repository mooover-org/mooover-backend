from typing import List

from corelib.domain.errors import NotFoundError, DuplicateError
from corelib.domain.models import User, Group
from corelib.repositories import Repository
from neo4j import Neo4jDriver, GraphDatabase, Result

from app.config import AppConfig


class Neo4jUserRepository(Repository):
    """Neo4J repository for users"""

    driver: Neo4jDriver

    def __init__(self, driver: Neo4jDriver = GraphDatabase.driver(uri=AppConfig().neo4j_config['HOST'], auth=(
            AppConfig().neo4j_config['USER'], AppConfig().neo4j_config['PASSWORD']))) -> None:
        self.driver = driver
        super().__init__({})

    def get_one(self, user_id: str) -> User:
        """
        Get one user by id

        :param user_id: The id of the user
        :return: The user
        :raises NotFoundError: If the user does not exist
        """

        def _get_user(tx, primary_key: str):
            result: Result = tx.run(f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                                    f"RETURN u "
                                    f"LIMIT 1")
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
            result = tx.run(f"MATCH (u:User) "
                            f"RETURN u")
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
            tx.run(f"CREATE (u:User {user.as_str_dict()})", )

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
            tx.run(f"MATCH (u:User {{{User.__primarykey__}: "
                   f"'{getattr(user, User.__primarykey__)}'}}) "
                   f"SET u = {user.as_str_dict()}")

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
            tx.run(f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                   f"DETACH DELETE u")

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
            result = tx.run(f"MATCH (u:User {{{User.__primarykey__}: '{primary_key}'}}) "
                            f"-[:MEMBER_OF]->(g:Group) "
                            f"RETURN g", )
            return [Group(**record.data()['g']) for record in result]

        self.get_one(user_id)
        with self.driver.session() as session:
            return session.read_transaction(_get_groups_of_user, user_id)

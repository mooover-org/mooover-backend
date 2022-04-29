from app.domain.models import User
from app.repositories import Repository


class UserServices:
    """The services associated with the user related operations"""

    def __init__(self, repo=Repository()) -> None:
        self.repo = repo

    def get_user(self, user_id: str) -> User:
        """
        Gets a user by id

        :param user_id: the id of the user
        :return: the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        return self.repo.get_one(user_id)

    def add_user(self, user: User) -> None:
        """
        Adds a user

        :param user: the user to be added
        :return: None
        :raises DuplicateError: if the user already exists in the repository
        """
        self.repo.add(user)

    def update_user(self, user_id: str, user: User) -> None:
        """
        Updates a user

        :param user_id: the id of the user
        :param user: the user with the updated values
        :return: None
        :raises NotFoundError: if the user cannot be found in the repository
        """
        user.id = user_id
        self.repo.update(user)

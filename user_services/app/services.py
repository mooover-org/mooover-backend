from app.domain.users import User
from app.repositories import MockUserRepository


class UserServices:
    """The services associated with the user related operations"""

    def __init__(self, repo=MockUserRepository()) -> None:
        self.repo = repo

    def get_user(self, user_id: int) -> User:
        """
        Gets a user by id.

        :param user_id: the id of the user
        :return: the user
        "raises NotFoundError: if the user cannot be found in the repository
        """
        return self.repo.find_one(user_id)

    def add_user(self, user: User):
        """
        Adds a user.

        :param user: the user to be added
        :return: the added user
        "raises DuplicateError: if the user already exists in the repository
        """
        return self.repo.add_user(user)

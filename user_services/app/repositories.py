from app.domain.errors import NotFoundError, DuplicateError
from app.domain.users import User


class MockUserRepository:
    """A user repository that mocks the data. Stores 3 default user in memory"""
    users = [
        User(**{"user_id": 1, "name": "user 1"}),
        User(**{"user_id": 2, "name": "user 2"})
    ]

    def find_one(self, user_id: int) -> User:
        """
        Finds the first user with the given id.

        :param user_id: the id of the user
        :return: the user
        :raises NotFoundError: if there is no user with that id in the repository
        """
        for user in self.users:
            if user_id == user.user_id:
                return user
        raise NotFoundError("user not found")

    def add_user(self, user: User):
        """
        Adds a user to the repo.

        :param user: the user to be added
        :return: the added user
        :raises DuplicateError: if there is user with that id in the repository already
        """
        try:
            self.find_one(user.user_id)
            raise DuplicateError("user already exists")
        except NotFoundError:
            self.users.append(user)
            return user

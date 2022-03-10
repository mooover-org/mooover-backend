from app.domain.errors import NotFoundError
from app.domain.users import User


class MockUserRepository:
    """A user repository that mocks the data. Stores 3 default user in memory"""
    users = [User(**{"user_id": 1}), User(**{"user_id": 2}),
             User(**{"user_id": 3})]

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
        raise NotFoundError

from typing import List

from corelib.domain.errors import NoContentError
from corelib.domain.models import User, Group
from corelib.repositories import Repository


class UserServices:
    """The services associated with the user related operations"""

    def __init__(self, repo=Repository({})) -> None:
        self.user_repo = repo

    def get_user(self, user_id: str) -> User:
        """
        Gets a user by its id

        :param user_id: the id of the user
        :return: the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        return self.user_repo.get_one(user_id)

    def get_users(self) -> List[User]:
        """
        Gets all the users

        :return: the users
        """
        return self.user_repo.get_all()

    def add_user(self, sub: str, name: str, given_name: str, family_name: str, nickname: str, email: str,
                 picture: str) -> None:
        """
        Adds a user with default values (0 steps, 5000 daily steps goal, no
        group)

        :param sub: the sub of the user
        :param name: the name of the user
        :param given_name: the given name of the user
        :param family_name: the family name of the user
        :param nickname: the nickname of the user
        :param email: the email of the user
        :param picture: the picture of the user
        :return: None
        :raises DuplicateError: if the user already exists in the repository
        :raises ValueError: if the user data is not valid
        """
        user = User(sub=sub, name=name, given_name=given_name, family_name=family_name, nickname=nickname, email=email,
                    picture=picture, )
        self.user_repo.add(user)

    def update_user(self, sub: str, name: str, given_name: str, family_name: str, nickname: str, email: str,
                    picture: str, today_steps: int, daily_steps_goal: int, this_week_steps: int, weekly_steps_goal: int,
                    app_theme: str) -> None:
        """
        Updates a user

        :param sub: the sub of the user
        :param name: the name of the user
        :param given_name: the given name of the user
        :param family_name: the family name of the user
        :param nickname: the nickname of the user
        :param email: the email of the user
        :param picture: the picture of the user
        :param today_steps: the steps of the user for today
        :param daily_steps_goal: the daily steps goal of the user
        :param this_week_steps: the steps of the user for this week
        :param weekly_steps_goal: the weekly steps goal of the user
        :param app_theme: the app theme of the user
        :return: None
        :raises NotFoundError: if the user cannot be found in the repository
        :raises ValueError: if the user data is not valid
        """
        user = User(sub=sub, name=name, given_name=given_name, family_name=family_name, nickname=nickname, email=email,
                    picture=picture, today_steps=today_steps, daily_steps_goal=daily_steps_goal,
                    this_week_steps=this_week_steps, weekly_steps_goal=weekly_steps_goal, app_theme=app_theme)
        self.user_repo.update(user)

    def get_group_of_user(self, user_id: str) -> Group:
        """
        Gets the group of a user

        :param user_id: the id of the user
        :return: the group of the user
        :raises NotFoundError: if the user cannot be found in the repository
        :raises NoContentError: if the user has no group
        """
        user = self.user_repo.get_one(user_id)
        groups = self.user_repo.get_groups_of_user(user.id)
        if len(groups) == 0:
            raise NoContentError("The user has no group")
        return groups[0]

    def get_user_steps(self, user_id: str) -> (int, int):
        """
        Gets the steps of a user

        :param user_id: the id of the user
        :return: the steps of the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        user = self.user_repo.get_one(user_id)
        return user.today_steps, user.this_week_steps

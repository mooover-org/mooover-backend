from app.domain.models import User, Group
from app.repositories import Repository


class UserServices:
    """The services associated with the user related operations"""

    def __init__(self, repo=Repository()) -> None:
        self.repo = repo

    def get_user(self, sub: str) -> User:
        """
        Gets a user by its sub

        :param sub: the sub of the user
        :return: the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        return self.repo.get_one(sub)

    def add_user(self, sub: str, name: str, given_name: str, family_name: str,
                 nickname: str, email: str, picture: str) -> None:
        """
        Adds a user with default values (0 steps, 5000 daily steps goal, no group)

        :param sub: the sub of the user
        :param name: the name of the user
        :param given_name: the given name of the user
        :param family_name: the family name of the user
        :param nickname: the nickname of the user
        :param email: the email of the user
        :param picture: the picture of the user
        :return: None
        :raises DuplicateError: if the user already exists in the repository
        """
        user = User()
        user.sub = sub
        user.name = name
        user.given_name = given_name
        user.family_name = family_name
        user.nickname = nickname
        user.email = email
        user.picture = picture
        user.steps = 0
        user.daily_steps_goal = 5000
        user.app_theme = "light"
        self.repo.add(user)

    def update_user(self, sub: str, name: str, given_name: str, family_name: str,
                    nickname: str, email: str, picture: str, steps: int, daily_steps_goal: int,
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
        :param steps: the steps of the user
        :param daily_steps_goal: the daily steps goal of the user
        :param app_theme: the app theme of the user
        :return: None
        :raises NotFoundError: if the user cannot be found in the repository
        """
        user = User()
        user.sub = sub
        user.name = name
        user.given_name = given_name
        user.family_name = family_name
        user.nickname = nickname
        user.email = email
        user.picture = picture
        user.steps = steps
        user.daily_steps_goal = daily_steps_goal
        user.app_theme = app_theme
        self.repo.update(user)

    def get_user_group(self, sub: str) -> Group:
        """
        Gets the group of a user

        :param sub: the sub of the user
        :return: the group of the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        user = self.get_user(sub)
        return user.member_of[0]


class GroupServices:
    """The services associated with the group related operations"""

    def __init__(self, repo=Repository()) -> None:
        self.repo = repo

    def get_group(self, nickname: str) -> Group:
        """
        Gets a group by its nickname

        :param nickname: the nickname of the group
        :return: the group
        :raises NotFoundError: if the group cannot be found in the repository
        """
        return self.repo.get_one(nickname)

    def add_group(self, user: User, name: str, nickname: str) -> None:
        """
        Adds a group with default values (0 steps, 5000 daily steps goal, 35000 weekly steps goal, 1 members)

        :param user: the user who creates the group
        :param name: the name of the group
        :param nickname: the nickname of the group
        :return: None
        :raises DuplicateError: if the group already exists in the repository
        """
        group = Group()
        group.name = name
        group.nickname = nickname
        group.steps = 0
        group.daily_steps_goal = 5000
        group.weekly_steps_goal = 35000
        group.members.add(user)
        self.repo.add(group)

    def update_group(self, nickname: str, name: str, steps: int, daily_steps_goal: int,
                     weekly_steps_goal: int) -> None:
        """
        Updates a group

        :param nickname: the nickname of the group
        :param name: the name of the group
        :param steps: the steps of the group
        :param daily_steps_goal: the daily steps goal of the group
        :param weekly_steps_goal: the weekly steps goal of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        """
        group = Group()
        group.nickname = nickname
        group.name = name
        group.steps = steps
        group.daily_steps_goal = daily_steps_goal
        group.weekly_steps_goal = weekly_steps_goal
        self.repo.update(group)

    def delete_group(self, nickname: str) -> None:
        """
        Deletes a group

        :param nickname: the nickname of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        """
        self.repo.delete(nickname)

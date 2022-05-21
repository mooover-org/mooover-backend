from typing import List

from app.domain.errors import NotFoundError, DuplicateError
from app.domain.models import User, Group
from app.repositories import Neo4jUserRepository, Neo4jGroupRepository


class UserServices:
    """The services associated with the user related operations"""

    def __init__(self, repo=Neo4jUserRepository()) -> None:
        self.repo = repo

    def get_user(self, sub: str) -> User:
        """
        Gets a user by its sub

        :param sub: the sub of the user
        :return: the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        return self.repo.get_one(sub)

    def get_users(self) -> List[User]:
        """
        Gets all the users

        :return: the users
        """
        return self.repo.get_all()

    def add_user(self, sub: str, name: str, given_name: str, family_name: str,
                 nickname: str, email: str, picture: str) -> None:
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
        user = User(sub=sub, name=name, given_name=given_name,
                    family_name=family_name, nickname=nickname, email=email,
                    picture=picture, )
        self.repo.add(user)

    def update_user(self, sub: str, name: str, given_name: str,
                    family_name: str, nickname: str, email: str, picture: str,
                    steps: int, daily_steps_goal: int, app_theme: str) -> None:
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
        :raises ValueError: if the user data is not valid
        """
        user = User(sub=sub, name=name, given_name=given_name,
                    family_name=family_name, nickname=nickname, email=email,
                    picture=picture, steps=steps,
                    daily_steps_goal=daily_steps_goal, app_theme=app_theme)
        self.repo.update(user)

    def get_group_of_user(self, sub: str) -> Group:
        """
        Gets the group of a user

        :param sub: the sub of the user
        :return: the group of the user
        :raises NotFoundError: if the user cannot be found in the repository
        """
        user = self.repo.get_one(sub)
        groups = self.repo.get_groups_of_user(user.sub)
        if len(groups) == 0:
            raise NotFoundError("The user has no group")
        return groups[0]


class GroupServices:
    """The services associated with the group related operations"""

    def __init__(self, group_repo=Neo4jGroupRepository(),
                 user_repo=Neo4jUserRepository()) -> None:
        self.group_repo = group_repo
        self.user_repo = user_repo

    def get_group(self, nickname: str) -> Group:
        """
        Gets a group by its nickname

        :param nickname: the nickname of the group
        :return: the group
        :raises NotFoundError: if the group cannot be found in the repository
        """
        return self.group_repo.get_one(nickname)

    def add_group(self, user: User, nickname: str, name: str) -> None:
        """
        Adds a group with default values (0 steps, 5000 daily steps goal, 35000
        weekly steps goal, 1 members)

        :param user: the user who creates the group
        :param nickname: the nickname of the group
        :param name: the name of the group
        :return: None
        :raises DuplicateError: if the group already exists in the repository or
        if the user already has a group
        :raises ValueError: if the group data is not valid
        """
        if self.user_repo.get_groups_of_user(user.sub):
            raise DuplicateError("The user already has a group")
        group = Group(nickname=nickname, name=name)
        self.group_repo.add(group)
        self.group_repo.add_member_to_group(user.sub, group.nickname)

    def update_group(self, nickname: str, name: str, steps: int,
                     daily_steps_goal: int, weekly_steps_goal: int) -> None:
        """
        Updates a group

        :param nickname: the nickname of the group
        :param name: the name of the group
        :param steps: the steps of the group
        :param daily_steps_goal: the daily steps goal of the group
        :param weekly_steps_goal: the weekly steps goal of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        :raises ValueError: if the group data is not valid
        """
        group = Group(nickname=nickname, name=name, steps=steps,
                      daily_steps_goal=daily_steps_goal,
                      weekly_steps_goal=weekly_steps_goal)
        self.group_repo.update(group)

    def delete_group(self, nickname: str) -> None:
        """
        Deletes a group

        :param nickname: the nickname of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        """
        self.group_repo.delete(nickname)

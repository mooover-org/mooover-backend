from typing import List

import httpx
from corelib.domain.errors import DuplicateError
from corelib.domain.models import User, Group
from fastapi import HTTPException

from app.config import AppConfig
from app.repositories import Neo4jGroupRepository

client = httpx.Client()


class GroupServices:
    """The services associated with the group related operations"""

    def __init__(self, group_repo: Neo4jGroupRepository) -> None:
        self.group_repo = group_repo

    def get_group(self, group_id: str) -> Group:
        """
        Gets a group by its id

        :param group_id: the id of the group
        :return: the group
        :raises NotFoundError: if the group cannot be found in the repository
        """
        return self.group_repo.get_one(group_id)

    def get_groups(self, nickname_filter: str = "", name_also: bool = True, loose: bool = True) -> List[Group]:
        """
        Gets multiple groups, with or without a filter applied

        :param nickname_filter: the nickname filter
        :param name_also: if the name also must be checked
        :param loose: if the filter should match parts of the nickname

        :return: the groups
        """
        groups = self.group_repo.get_all()
        if nickname_filter and nickname_filter != "":
            filtered_groups = []
            for group in groups:
                if loose:
                    if nickname_filter in group.nickname:
                        filtered_groups.append(group)
                    elif name_also and nickname_filter in group.name:
                        filtered_groups.append(group)
                else:
                    if nickname_filter == group.nickname:
                        filtered_groups.append(group)
                    elif name_also and nickname_filter == group.name:
                        filtered_groups.append(group)
            return filtered_groups
        return groups

    def add_group(self, user_id: str, nickname: str, name: str, bearer_token: str) -> None:
        """
        Adds a group with default values (0 steps, 5000 daily steps goal, 35000
        weekly steps goal, 1 members)

        :param user_id: the id of the user that creates the group
        :param nickname: the nickname of the group
        :param name: the name of the group
        :param bearer_token: the authorization bearer token
        :return: None
        :raises DuplicateError: if the group already exists in the repository or
        if the user already has a group
        :raises ValueError: if the group data is not valid
        :raises NotFoundError: if the user cannot be found in the repository
        """
        if self._get_group_of_user(user_id, bearer_token) is None:
            raise DuplicateError("The user already has a group")
        group = Group(nickname=nickname, name=name)
        self.group_repo.add(group)
        self.group_repo.add_member_to_group(user_id, group.id)

    def update_group(self, nickname: str, name: str, today_steps: int, daily_steps_goal: int, this_week_steps: int,
                     weekly_steps_goal: int) -> None:
        """
        Updates a group

        :param nickname: the nickname of the group
        :param name: the name of the group
        :param today_steps: the steps of the group for today
        :param daily_steps_goal: the daily steps goal of the group
        :param this_week_steps: the steps of the group for this week
        :param weekly_steps_goal: the weekly steps goal of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        :raises ValueError: if the group data is not valid
        """
        group = Group(nickname=nickname, name=name, today_steps=today_steps, daily_steps_goal=daily_steps_goal,
                      this_week_steps=this_week_steps, weekly_steps_goal=weekly_steps_goal)
        self.group_repo.update(group)

    def delete_group(self, group_id: str) -> None:
        """
        Deletes a group

        :param group_id: the id of the group
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        """
        self.group_repo.delete(group_id)

    def get_members_of_group(self, group_id: str) -> List[User]:
        """
        Gets the members of a group

        :param group_id: the id of the group
        :return: the members of the group
        :raises NotFoundError: if the group cannot be found in the repository
        """
        return self.group_repo.get_members_of_group(group_id)

    def add_member_to_group(self, user_id: str, group_id: str, bearer_token: str) -> None:
        """
        Adds a member to a group

        :param user_id: the id of the user
        :param group_id: the id of the group
        :param bearer_token: the authorization bearer token
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        :raises DuplicateError: if the user is already a member of this group or another group
        """
        group = self._get_group_of_user(user_id, bearer_token)
        if group is not None:
            if group.id == group_id:
                raise DuplicateError("The user is already a member of the group")
            raise DuplicateError("The user is already a member of a group")
        self.group_repo.add_member_to_group(user_id, group_id)
        # update steps
        user = self._get_one_user(user_id, bearer_token)
        group = self.group_repo.get_one(group_id)
        group.today_steps += user.today_steps
        group.this_week_steps += user.this_week_steps
        self.group_repo.update(group)

    def remove_member_from_group(self, user_id: str, group_id: str, bearer_token: str) -> None:
        """
        Removes a member from a group

        :param user_id: the id of the member
        :param group_id: the id of the group
        :param bearer_token: the authorization bearer token
        :return: None
        :raises NotFoundError: if the group cannot be found in the repository
        :raises NotFoundError: if the member cannot be found in the repository
        """
        self.group_repo.remove_member_from_group(user_id, group_id)
        if not self.group_repo.get_members_of_group(group_id):
            self.group_repo.delete(group_id)
        else:
            # update steps
            user = self._get_one_user(user_id, bearer_token)
            group = self.group_repo.get_one(group_id)
            group.today_steps -= user.today_steps
            group.this_week_steps -= user.this_week_steps
            self.group_repo.update(group)

    def _get_one_user(self, user_id: str, bearer_token: str) -> User:
        response = client.get(f'{AppConfig().user_services_url}/{user_id}',
                              headers={"Authorization": f"Bearer {bearer_token}"})
        if response.status_code == 200:
            return User.from_dict(response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    def _get_group_of_user(self, user_id: str, bearer_token: str) -> Group | None:
        response = client.get(f'{AppConfig().user_services_url}/{user_id}/group',
                              headers={"Authorization": f"Bearer {bearer_token}"})
        if response.status_code == 204:
            return None
        elif response.status_code != 200:
            return Group.from_dict(response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

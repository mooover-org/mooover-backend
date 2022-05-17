import httpx

from app.domain.errors import NotFoundError
from app.utils.config import AppConfig


class StepsServices:
    """The services associated with the steps related operations"""

    def __init__(self) -> None:
        self.user_services_url = AppConfig().app_config["USER_SERVICES_URL"]

    def get_steps(self, user_id: str, credentials: str) -> int:
        """
        Get the steps for a user

        :param user_id: The user id
        :param credentials: The authorization token
        :return: The steps
        :raises NotFoundError: If the user does not exist
        """
        response = httpx.get(self.user_services_url + f"/{user_id}",
                             headers={"Authorization": "Bearer " + credentials})
        if response.status_code != 200:
            raise NotFoundError(f"User with id {user_id} does not exist")
        return response.json()["steps"]

    def update_steps(self, user_id: str, steps: int, credentials: str) -> None:
        """
        Set the steps for a user

        :param user_id: The user id
        :param steps: The steps
        :param credentials: The authorization token
        :return: None
        :raises NotFoundError: If the user does not exist
        """
        response = httpx.get(self.user_services_url + f"/{user_id}",
                             headers={"Authorization": "Bearer " + credentials})
        if response.status_code != 200:
            raise NotFoundError(f"User with id {user_id} does not exist")
        user_dict = response.json()
        user_dict["steps"] = steps
        response = httpx.put(self.user_services_url + f"/{user_id}", json=user_dict,
                             headers={"Authorization": "Bearer " + credentials})
        if response.status_code != 200:
            raise NotFoundError(f"User with id {user_id} does not exist")

    def add_to_steps(self, user_id: str, steps: int, credentials: str) -> None:
        """
        Add to the user's current steps

        :param user_id: The user id
        :param steps: The steps to be added
        :param credentials: The authorization token
        :return: None
        :raises NotFoundError: If the user does not exist
        """
        response = httpx.get(self.user_services_url + f"/{user_id}",
                             headers={"Authorization": "Bearer " + credentials})
        if response.status_code != 200:
            raise NotFoundError(f"User with id {user_id} does not exist")
        user_dict = response.json()
        user_dict["steps"] += steps
        response = httpx.put(self.user_services_url + f"/{user_id}", json=user_dict,
                             headers={"Authorization": "Bearer " + credentials})
        if response.status_code != 200:
            raise NotFoundError(f"User with id {user_id} does not exist")

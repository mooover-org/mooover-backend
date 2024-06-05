from datetime import datetime, timedelta
from threading import Thread

import pause

from app.repositories import Neo4jStepsRepository


class StepsServices:
    """The services associated with the steps related operations"""

    def __init__(self, steps_repo_utils: Neo4jStepsRepository) -> None:
        self.steps_repo_utils = steps_repo_utils

    def add_new_steps(self, user_id: str, steps: int) -> None:
        """
        Adds new steps to the user

        :param user_id: the id of the user
        :param steps: the steps to add
        :return: None
        :raises NotFoundError: if the user cannot be found in the repository
        """
        self.steps_repo_utils.add_new_steps(user_id, steps)

    def run_background_tasks(self):
        """
        Runs the background tasks for the steps related operations

        :return: None
        """

        def _reset_today_steps():
            """
            Resets the today steps of all users and groups

            :return: None
            """
            while True:
                pause.until(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
                self.steps_repo_utils.reset_all_daily_steps()
                print("Today steps reset")

        def _reset_this_week_steps():
            """
            Resets this week's steps of all users and groups

            :return: None
            """
            while True:
                pause.until(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
                    days=(7 - datetime.now().weekday())))
                self.steps_repo_utils.reset_all_weekly_steps()
                print("This week's steps reset")

        thread1 = Thread(target=_reset_today_steps)
        thread2 = Thread(target=_reset_this_week_steps)
        thread1.start()
        thread2.start()

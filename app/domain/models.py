class User:
    """The base user model"""
    __primarykey__ = "sub"

    sub: str
    name: str
    given_name: str
    family_name: str
    nickname: str
    email: str
    picture: str
    today_steps: int
    daily_steps_goal: int
    this_week_steps: int
    weekly_steps_goal: int
    app_theme: str

    @property
    def id(self) -> str:
        return self.sub

    @id.setter
    def id(self, value):
        self.sub = value

    def __init__(self, sub: str, name: str, given_name: str, family_name: str,
                 nickname: str, email: str, picture: str, today_steps: int = 0,
                 daily_steps_goal: int = 5000, this_week_steps: int = 0,
                 weekly_steps_goal: int = 35000, app_theme: str = "light"):
        """
        Constructor

        :param sub: The sub of the user
        :param name: The name of the user
        :param given_name: The given name of the user
        :param family_name: The family name of the user
        :param nickname: The nickname of the user
        :param email: The email of the user
        :param picture: The picture of the user
        :param today_steps: The steps of the user for today (default: 0)
        :param daily_steps_goal: The daily steps goal of the user (default:
        5000)
        :param this_week_steps: The steps of the user for this week (default:
        0)
        :param weekly_steps_goal: The weekly steps goal of the user (default:
        35000)
        :param app_theme: The app theme of the user (default: "light")
        """
        self.sub = sub
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.nickname = nickname
        self.email = email
        self.picture = picture
        self.today_steps = today_steps
        self.daily_steps_goal = daily_steps_goal
        self.this_week_steps = this_week_steps
        self.weekly_steps_goal = weekly_steps_goal
        self.app_theme = app_theme
        self.validate()

    def validate(self) -> None:
        """
        Validate the user

        :return: None
        :raises ValueError: if invalid user data
        """
        if not self.sub or not self.name or not self.given_name or not \
                self.family_name or not self.nickname or not self.email or \
                not self.picture or self.today_steps < 0 or \
                self.daily_steps_goal < 0 or self.this_week_steps < 0 or \
                self.weekly_steps_goal < 0 or not self.app_theme:
            raise ValueError("Invalid user data")

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to user

        :param data: the data to convert
        :return: The user
        """
        return User(sub=data["sub"], name=data["name"],
                    given_name=data["given_name"],
                    family_name=data["family_name"], nickname=data["nickname"],
                    email=data["email"], picture=data["picture"],
                    today_steps=data.get("today_steps") or 0,
                    daily_steps_goal=data.get("daily_steps_goal") or 5000,
                    this_week_steps=data.get("this_week_steps") or 0,
                    weekly_steps_goal=data.get("weekly_steps_goal") or 35000,
                    app_theme=data.get("app_theme") or "light", )

    def as_dict(self) -> dict:
        """
        Convert user to dict

        :return: The dict representation of the user
        """
        return {"sub": self.sub, "name": self.name,
                "given_name": self.given_name, "family_name": self.family_name,
                "nickname": self.nickname, "email": self.email,
                "picture": self.picture, "today_steps": self.today_steps,
                "daily_steps_goal": self.daily_steps_goal,
                "this_week_steps": self.this_week_steps,
                "weekly_steps_goal": self.weekly_steps_goal,
                "app_theme": self.app_theme, }

    def as_str_dict(self) -> str:
        """
        Convert user to dict

        :return: The dict representation of the user
        """
        return f"{{sub: '{self.sub}', " \
               f"name: '{self.name}', " \
               f"given_name: '{self.given_name}', " \
               f"family_name: '{self.family_name}', " \
               f"nickname: '{self.nickname}', " \
               f"email: '{self.email}', " \
               f"picture: '{self.picture}', " \
               f"today_steps: {self.today_steps}, " \
               f"daily_steps_goal: {self.daily_steps_goal}, " \
               f"this_week_steps: {self.this_week_steps}, " \
               f"weekly_steps_goal: {self.weekly_steps_goal}, " \
               f"app_theme: '{self.app_theme}'}}"


class Group:
    """The base group model"""
    __primarykey__ = "nickname"

    nickname: str
    name: str
    today_steps: int
    daily_steps_goal: int
    this_week_steps: int
    weekly_steps_goal: int

    @property
    def id(self) -> str:
        return self.nickname

    @id.setter
    def id(self, value):
        self.nickname = value

    def __init__(self, nickname: str, name: str, today_steps: int = 0,
                 daily_steps_goal: int = 5000, this_week_steps: int = 0,
                 weekly_steps_goal: int = 35000):
        """
        Constructor

        :param nickname: The nickname of the group
        :param name: The name of the group
        :param today_steps: The steps of the group for today (default: 0)
        :param daily_steps_goal: The daily steps goal of the group (default:
        5000)
        :param this_week_steps: The steps of the group for this week (default:
        0)
        :param weekly_steps_goal: The weekly steps goal of the group (default:
        35000)
        """
        self.nickname = nickname
        self.name = name
        self.today_steps = today_steps
        self.daily_steps_goal = daily_steps_goal
        self.this_week_steps = this_week_steps
        self.weekly_steps_goal = weekly_steps_goal
        self.validate()

    def validate(self) -> None:
        """
        Validate the group

        :return: None
        :raises ValueError: if invalid group data
        """
        if not self.nickname or not self.name or self.today_steps < 0 or \
                self.daily_steps_goal < 0 or self.this_week_steps < 0 or \
                self.weekly_steps_goal < 0:
            raise ValueError("Invalid group data")

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to group

        :param data: the data to convert
        :return: The group
        """
        return Group(nickname=data["nickname"], name=data["name"],
                     today_steps=data.get("today_steps") or 0,
                     daily_steps_goal=data.get("daily_steps_goal") or 5000,
                     this_week_steps=data.get("this_week_steps") or 0,
                     weekly_steps_goal=data.get("weekly_steps_goal") or 35000, )

    def as_dict(self) -> dict:
        """
        Convert group to dict

        :return: The dict representation of the group
        """
        return {"nickname": self.nickname, "name": self.name,
                "today_steps": self.today_steps,
                "daily_steps_goal": self.daily_steps_goal,
                "this_week_steps": self.this_week_steps,
                "weekly_steps_goal": self.weekly_steps_goal, }

    def as_str_dict(self) -> str:
        """
        Convert group to string dictionary

        :return: The string dictionary representation of the group
        """
        return f"{{nickname: '{self.nickname}', " \
               f"name: '{self.name}', " \
               f"today_steps: {self.today_steps}, " \
               f"daily_steps_goal: {self.daily_steps_goal}, " \
               f"this_week_steps: {self.this_week_steps}, " \
               f"weekly_steps_goal: {self.weekly_steps_goal}}}"

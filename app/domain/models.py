class Group:
    """The base group model"""
    nickname: str
    name: str
    steps: int
    daily_steps_goal: int
    weekly_steps_goal: int

    members = RelatedFrom("User", "MEMBER_OF")

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to group

        :param data: the data to convert
        :return: The group
        """
        group = Group()
        group.nickname = data.get("nickname")
        group.name = data.get("name")
        group.steps = data.get("steps")
        group.daily_steps_goal = data.get("daily_steps_goal")
        group.weekly_steps_goal = data.get("weekly_steps_goal")
        return group

    def to_dict(self) -> dict:
        """
        Convert group to dict

        :return: The dict representation of the group
        """
        return {
            "nickname": self.nickname,
            "name": self.name,
            "steps": self.steps,
            "daily_steps_goal": self.daily_steps_goal,
            "weekly_steps_goal": self.weekly_steps_goal,
        }


class User(Model):
    """The base user model"""
    __primarykey__ = "sub"

    sub: str = Property()
    name: str = Property()
    given_name: str = Property()
    family_name: str = Property()
    nickname: str = Property()
    email: str = Property()
    picture: str = Property()
    steps: int = Property()
    daily_steps_goal: int = Property()
    app_theme: str = Property()

    member_of = RelatedTo(Group)

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to user

        :param data: the data to convert
        :return: The user
        """
        user = User()
        user.sub = data.get("sub")
        user.name = data.get("name")
        user.given_name = data.get("given_name")
        user.family_name = data.get("family_name")
        user.nickname = data.get("nickname")
        user.email = data.get("email")
        user.picture = data.get("picture")
        user.steps = data.get("steps")
        user.daily_steps_goal = data.get("daily_steps_goal")
        user.app_theme = data.get("app_theme")
        return user

    def to_dict(self) -> dict:
        """
        Convert user to dict

        :return: The dict representation of the user
        """
        return {
            "sub": self.sub,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "nickname": self.nickname,
            "email": self.email,
            "picture": self.picture,
            "steps": self.steps,
            "daily_steps_goal": self.daily_steps_goal,
            "app_theme": self.app_theme,
        }

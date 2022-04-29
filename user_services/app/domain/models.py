from py2neo.ogm import Property, Model


class Entity(Model):
    """Base entity class"""
    __primarykey__ = "id"

    id: str = Property()

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to entity

        :param data: The dict to convert
        :return: The entity
        """
        entity = Entity()
        entity.id = data["id"]
        return entity

    def to_dict(self) -> dict:
        """
        Convert entity to dict

        :return: The entity as dict
        """
        return {
            "id": self.id,
        }


class User(Entity):
    """The base user model"""
    name: str = Property()
    given_name: str = Property()
    family_name: str = Property()
    nickname: str = Property()
    email: str = Property()
    picture: str = Property()

    steps: int = Property()

    @staticmethod
    def from_dict(data: dict):
        """
        Convert dict to user

        :param data: the data to convert
        :return: The user
        """
        user = User()
        user.id = data.get("id")
        user.name = data.get("name")
        user.given_name = data.get("given_name")
        user.family_name = data.get("family_name")
        user.nickname = data.get("nickname")
        user.email = data.get("email")
        user.picture = data.get("picture")
        user.steps = data.get("steps")
        return user

    def to_dict(self) -> dict:
        """
        Convert user to dict

        :return: The dict representation of the user
        """
        return {
            "id": self.id,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "nickname": self.nickname,
            "email": self.email,
            "picture": self.picture,
            "steps": self.steps,
        }

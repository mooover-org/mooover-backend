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

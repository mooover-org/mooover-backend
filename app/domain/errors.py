class AppError(Exception):
    """The default app error"""

    def __init__(self, message="an error occurred") -> None:
        super().__init__(message)


class NotFoundError(AppError):
    """Error thrown when an entity or resource could not be found"""

    def __init__(self, message="entity not found") -> None:
        super().__init__(message)


class DuplicateError(AppError):
    """Error thrown when an entity or resource already exists"""

    def __init__(self, message="entity already exists") -> None:
        super().__init__(message)


class NoContentError(AppError):
    """Error thrown when an entity or resource is empty"""

    def __init__(self, message="entity is empty") -> None:
        super().__init__(message)

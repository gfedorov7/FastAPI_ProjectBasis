from src.types import ID


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppException):
    def __init__(self, model_name: str, entity_id: ID):
        message = f"{model_name} with ID {entity_id} not found"
        super().__init__(message, status_code=404)

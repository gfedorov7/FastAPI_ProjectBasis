

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundRecord(AppException):
    def __init__(self, model: str):
        message = f"Not found record in model {model}"
        status_code = 404
        super().__init__(message, status_code)

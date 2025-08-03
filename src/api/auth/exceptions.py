from src.exceptions import AppException


class ExpiredTokenException(AppException):
    def __init__(self):
        message = "Expired token"
        super().__init__(message, 401)

class DecodeTokenException(AppException):
    def __init__(self):
        message = "Cannot decode token"
        super().__init__(message, 400)

class InvalidTokenException(AppException):
    def __init__(self):
        message = "Invalid token"
        super().__init__(message, 401)

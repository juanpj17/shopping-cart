from core.application.exceptions.application_exception import ApplicationException

class EmptyTokenError(ApplicationException):
    def __init__(self, message='Token is empty.'):
        self.message = message
        super().__init__(self.message)
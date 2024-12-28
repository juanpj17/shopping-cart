from core.application.exceptions.application_exception import ApplicationException

class UserNotManager(ApplicationException):
    def __init__(self, message='This endpoint is to update managers only'):
        self.message = message
        super().__init__(self.message)
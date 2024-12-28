from core.application.exceptions.application_exception import ApplicationException

class SuperUserAlreadyCreated(ApplicationException):
    def __init__(self, message='Superuser can be created just once'):
        self.message = message
        super().__init__(self.message)
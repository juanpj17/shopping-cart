from core.application.exceptions.application_exception import ApplicationException

class NotEnoughProductError(ApplicationException):
    def __init__(self, id: str, message='Not enough product: '):
        self.message = message + id
        super().__init__(self.message)
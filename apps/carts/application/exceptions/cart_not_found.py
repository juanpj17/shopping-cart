from core.application.exceptions.application_exception import ApplicationException

class CartNotFoundError(ApplicationException):
    def __init__(self, message='Cart not found'):
        self.message = message 
        super().__init__(self.message)
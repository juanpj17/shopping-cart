from core.application.exceptions.application_exception import ApplicationException

class OrdersNotFoundError(ApplicationException):
    def __init__(self, message='Orders not found'):
        self.message = message 
        super().__init__(self.message)
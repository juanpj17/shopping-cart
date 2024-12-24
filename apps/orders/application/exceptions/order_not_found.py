from core.application.exceptions.application_exception import ApplicationException

class OrderNotFoundError(ApplicationException):
    def __init__(self, message='Order not found'):
        self.message = message 
        super().__init__(self.message)
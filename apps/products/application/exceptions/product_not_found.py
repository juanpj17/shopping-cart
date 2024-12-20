from core.application.exceptions.application_exception import ApplicationException

class ProductNotFoundError(ApplicationException):
    def __init__(self, message='Product not found'):
        self.message = message
        super().__init__(self.message)
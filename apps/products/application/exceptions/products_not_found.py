from core.application.exceptions.application_exception import ApplicationException

class ProductsNotFoundError(ApplicationException):
    def __init__(self, message='Products not found'):
        self.message = message
        super().__init__(self.message)
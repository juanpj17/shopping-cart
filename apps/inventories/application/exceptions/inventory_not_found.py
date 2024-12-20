from core.application.exceptions.application_exception import ApplicationException

class InventoryNotFoundError(ApplicationException):
    def __init__(self, message='Inventory not found'):
        self.message = message
        super().__init__(self.message)
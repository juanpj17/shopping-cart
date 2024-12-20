from core.application.exceptions.application_exception import ApplicationException

class InventoriesNotFoundError(ApplicationException):
    def __init__(self, message='Inventories not found'):
        self.message = message
        super().__init__(self.message)
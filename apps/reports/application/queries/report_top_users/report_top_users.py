from typing import List, Tuple
from apps.users.application.exceptions.user_not_found import UserNotFoundError
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTopUsers(Service[None, List[Tuple[str, int]]]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        report = self.report_repository.get_top_users()
        if not report: Result[List[Tuple[str, int]]].make_failure(error = UserNotFoundError())

        return Result[List[Tuple[str, int]]].make_success(value = report)
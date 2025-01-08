from dataclasses import dataclass

from apps.reports.domain.top_user_count import TopUserCount



@dataclass
class TopUser:
    top_users: list[TopUserCount]
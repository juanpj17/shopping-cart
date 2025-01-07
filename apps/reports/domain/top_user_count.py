from dataclasses import dataclass


@dataclass
class TopUserCount:
    name: str
    total_orders: int
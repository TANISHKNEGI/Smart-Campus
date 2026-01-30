from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    user_id: str
    name: str
    role: str  # "Faculty" or "Student"
    priority: int  # lower = higher priority


@dataclass
class Resource:
    resource_id: str
    name: str
    capacity: Optional[int] = None


@dataclass(order=True)
class BookingRequest:
    sort_index: tuple = field(init=False, repr=False)
    request_id: str
    user_id: str
    resource_id: str
    start_time: datetime
    end_time: datetime
    request_time: datetime
    priority: int

    def __post_init__(self):
        self.sort_index = (
            self.priority,
            self.request_time,
            self.user_id,
            self.resource_id
        )


@dataclass
class Booking:
    booking_id: str
    user_id: str
    resource_id: str
    start_time: datetime
    end_time: datetime

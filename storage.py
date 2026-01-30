import json
from datetime import datetime
from models import User, Resource, Booking
from scheduler import Scheduler


def save_state(scheduler: Scheduler, filename="state.json"):
    data = {
        "users": [u.__dict__ for u in scheduler.users.values()],
        "resources": [r.__dict__ for r in scheduler.resources.values()],
        "bookings": [
            {
                **b.__dict__,
                "start_time": b.start_time.isoformat(),
                "end_time": b.end_time.isoformat()
            }
            for b in scheduler.bookings.values()
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_state(scheduler: Scheduler, filename="state.json"):
    with open(filename) as f:
        data = json.load(f)

    for u in data["users"]:
        scheduler.users[u["user_id"]] = User(**u)

    for r in data["resources"]:
        scheduler.resources[r["resource_id"]] = Resource(**r)
        scheduler.allocations[r["resource_id"]] = []

    for b in data["bookings"]:
        booking = Booking(
            booking_id=b["booking_id"],
            user_id=b["user_id"],
            resource_id=b["resource_id"],
            start_time=datetime.fromisoformat(b["start_time"]),
            end_time=datetime.fromisoformat(b["end_time"])
        )
        scheduler.bookings[booking.booking_id] = booking
        scheduler.allocations[booking.resource_id].append(booking)

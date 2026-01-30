import heapq
from collections import deque
from typing import Dict, List
from datetime import datetime
from models import User, Resource, BookingRequest, Booking
from utils import is_overlap
import uuid


class Scheduler:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.bookings: Dict[str, Booking] = {}
        self.allocations: Dict[str, List[Booking]] = {}
        self.request_heap: List[BookingRequest] = []
        self.waiting_queue = deque()

    # ---------- USER ----------
    def add_user(self, name: str, role: str) -> str:
        user_id = str(uuid.uuid4())
        priority = 0 if role.lower() == "faculty" else 1
        self.users[user_id] = User(user_id, name, role, priority)
        return user_id

    # ---------- RESOURCE ----------
    def add_resource(self, name: str, capacity=None) -> str:
        rid = str(uuid.uuid4())
        self.resources[rid] = Resource(rid, name, capacity)
        self.allocations[rid] = []
        return rid

    # ---------- REQUEST ----------
    def request_booking(self, user_id, resource_id, start, end):
        if user_id not in self.users:
            raise ValueError("Invalid user")
        if resource_id not in self.resources:
            raise ValueError("Invalid resource")
        if start >= end:
            raise ValueError("Invalid time window")

        req = BookingRequest(
            request_id=str(uuid.uuid4()),
            user_id=user_id,
            resource_id=resource_id,
            start_time=start,
            end_time=end,
            request_time=datetime.utcnow(),
            priority=self.users[user_id].priority
        )

        heapq.heappush(self.request_heap, req)
        return self._attempt_allocate()

    # ---------- ALLOCATION ----------
    def _attempt_allocate(self):
        if not self.request_heap:
            return None

        req = heapq.heappop(self.request_heap)
        existing = self.allocations[req.resource_id]

        # Check for conflicts
        conflicting_bookings = []
        for b in existing:
            if is_overlap(req.start_time, req.end_time, b.start_time, b.end_time):
                conflicting_bookings.append(b)

        # If no conflicts, book immediately
        if not conflicting_bookings:
            booking = Booking(
                booking_id=str(uuid.uuid4()),
                user_id=req.user_id,
                resource_id=req.resource_id,
                start_time=req.start_time,
                end_time=req.end_time
            )
            self.bookings[booking.booking_id] = booking
            self.allocations[req.resource_id].append(booking)
            self.allocations[req.resource_id].sort(key=lambda b: b.start_time)
            return f"CONFIRMED: {booking.booking_id}"

        # Handle conflicts with priority preemption
        req_user = self.users[req.user_id]
        can_preempt = False
        preempted_bookings = []

        for conflicting_booking in conflicting_bookings:
            conflicting_user = self.users[conflicting_booking.user_id]
            # Faculty (priority 0) can preempt Students (priority 1)
            if req_user.priority < conflicting_user.priority:
                can_preempt = True
                preempted_bookings.append(conflicting_booking)

        if can_preempt:
            # Remove preempted bookings
            for preempted in preempted_bookings:
                self.bookings.pop(preempted.booking_id)
                self.allocations[req.resource_id].remove(preempted)
                # Add preempted user back to waiting queue
                preempted_req = BookingRequest(
                    request_id=str(uuid.uuid4()),
                    user_id=preempted.user_id,
                    resource_id=preempted.resource_id,
                    start_time=preempted.start_time,
                    end_time=preempted.end_time,
                    request_time=datetime.utcnow(),
                    priority=self.users[preempted.user_id].priority
                )
                self.waiting_queue.append(preempted_req)

            # Confirm the higher priority booking
            booking = Booking(
                booking_id=str(uuid.uuid4()),
                user_id=req.user_id,
                resource_id=req.resource_id,
                start_time=req.start_time,
                end_time=req.end_time
            )
            self.bookings[booking.booking_id] = booking
            self.allocations[req.resource_id].append(booking)
            self.allocations[req.resource_id].sort(key=lambda b: b.start_time)
            
            preempted_names = [self.users[b.user_id].name for b in preempted_bookings]
            return f"CONFIRMED: {booking.booking_id} (preempted: {', '.join(preempted_names)})"

        # Cannot preempt, add to waiting queue
        self.waiting_queue.append(req)
        return f"WAITLISTED: {req.request_id}"

    # ---------- CANCELLATION ----------
    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise ValueError("Invalid booking ID")

        booking = self.bookings.pop(booking_id)
        self.allocations[booking.resource_id] = [
            b for b in self.allocations[booking.resource_id]
            if b.booking_id != booking_id
        ]

        self._promote_waiting()

    # ---------- WAITLIST PROMOTION ----------
    def _promote_waiting(self):
        temp = list(self.waiting_queue)
        self.waiting_queue.clear()
        heapq.heapify(temp)

        while temp:
            req = heapq.heappop(temp)
            conflict = False
            for b in self.allocations[req.resource_id]:
                if is_overlap(req.start_time, req.end_time, b.start_time, b.end_time):
                    conflict = True
                    break

            if not conflict:
                booking = Booking(
                    booking_id=str(uuid.uuid4()),
                    user_id=req.user_id,
                    resource_id=req.resource_id,
                    start_time=req.start_time,
                    end_time=req.end_time
                )
                self.bookings[booking.booking_id] = booking
                self.allocations[req.resource_id].append(booking)
            else:
                self.waiting_queue.append(req)

#!/usr/bin/env python3
"""
Smart Campus Resource Allocation System
A CLI-based system for managing campus resources with priority-based scheduling
"""

import heapq
import json
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from collections import deque
import itertools

@dataclass
class User:
    """User data model"""
    user_id: str
    name: str
    role: str  # "Student" or "Faculty"
    priority_score: int
    email: str
    created_at: str

@dataclass
class Resource:
    """Resource data model"""
    resource_id: str
    name: str
    capacity: int
    location: str
    description: str
    created_at: str

@dataclass
class BookingRequest:
    """Booking request data model"""
    request_id: str
    user_id: str
    resource_id: str
    start_time: datetime
    end_time: datetime
    request_timestamp: datetime
    status: str  # "pending", "confirmed", "cancelled", "waitlisted"
    priority_score: int

@dataclass
class Booking:
    """Confirmed booking data model"""
    booking_id: str
    request_id: str
    user_id: str
    resource_id: str
    start_time: datetime
    end_time: datetime
    confirmed_at: datetime

class SmartCampusSystem:
    """Main system class for Smart Campus Resource Allocation"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.bookings: Dict[str, Booking] = {}
        self.booking_requests: Dict[str, BookingRequest] = {}
        
        # Priority queue for scheduling (min-heap)
        # Format: (priority_score, request_timestamp, request_id)
        self.priority_queue = []
        
        # Waiting queues per resource
        self.waiting_queues: Dict[str, deque] = {}
        
        # Counter for tie-breaking in priority queue
        self.counter = itertools.count()
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize system with sample users and resources"""
        # Sample users
        sample_users = [
            ("user001", "Dr. Sarah Johnson", "Faculty", "sarah.johnson@university.edu"),
            ("user002", "Prof. Michael Chen", "Faculty", "michael.chen@university.edu"),
            ("user003", "Alice Smith", "Student", "alice.smith@student.university.edu"),
            ("user004", "Bob Wilson", "Student", "bob.wilson@student.university.edu"),
            ("user005", "Dr. Emily Davis", "Faculty", "emily.davis@university.edu"),
            ("user006", "Charlie Brown", "Student", "charlie.brown@student.university.edu"),
            ("user007", "Diana Martinez", "Student", "diana.martinez@student.university.edu"),
            ("user008", "Prof. James Taylor", "Faculty", "james.taylor@university.edu")
        ]
        
        for user_id, name, role, email in sample_users:
            self.add_user(user_id, name, role, email)
        
        # Sample resources
        sample_resources = [
            ("res001", "Computer Lab A", 30, "Building 1, Floor 2", "Main computer lab with 30 workstations"),
            ("res002", "Seminar Hall 1", 50, "Building 2, Floor 1", "Large seminar hall for presentations"),
            ("res003", "Conference Room B", 12, "Building 1, Floor 3", "Small conference room for meetings"),
            ("res004", "Physics Lab", 20, "Science Building, Floor 2", "Physics laboratory with equipment"),
            ("res005", "Library Study Room", 8, "Library, Floor 3", "Quiet study room for group work"),
            ("res006", "Auditorium", 200, "Main Building", "Large auditorium for events"),
            ("res007", "Chemistry Lab", 25, "Science Building, Floor 1", "Chemistry laboratory"),
            ("res008", "Meeting Room C", 6, "Administration Building", "Small meeting room")
        ]
        
        for res_id, name, capacity, location, description in sample_resources:
            self.add_resource(res_id, name, capacity, location, description)
    
    def _get_priority_score(self, role: str) -> int:
        """Calculate priority score based on user role"""
        if role == "Faculty":
            return 1  # Higher priority (lower number in min-heap)
        elif role == "Student":
            return 2  # Lower priority
        else:
            return 3  # Default lowest priority
    
    def add_user(self, user_id: str, name: str, role: str, email: str) -> bool:
        """Add a new user to the system"""
        if user_id in self.users:
            print(f"Error: User {user_id} already exists")
            return False
        
        if role not in ["Student", "Faculty"]:
            print("Error: Role must be 'Student' or 'Faculty'")
            return False
        
        priority_score = self._get_priority_score(role)
        user = User(
            user_id=user_id,
            name=name,
            role=role,
            priority_score=priority_score,
            email=email,
            created_at=datetime.now().isoformat()
        )
        
        self.users[user_id] = user
        print(f"User {name} ({role}) added successfully with priority score {priority_score}")
        return True
    
    def add_resource(self, resource_id: str, name: str, capacity: int, location: str, description: str) -> bool:
        """Add a new resource to the system"""
        if resource_id in self.resources:
            print(f"Error: Resource {resource_id} already exists")
            return False
        
        resource = Resource(
            resource_id=resource_id,
            name=name,
            capacity=capacity,
            location=location,
            description=description,
            created_at=datetime.now().isoformat()
        )
        
        self.resources[resource_id] = resource
        self.waiting_queues[resource_id] = deque()
        print(f"Resource '{name}' added successfully")
        return True
    
    def _validate_booking_request(self, user_id: str, resource_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Validate booking request parameters"""
        if user_id not in self.users:
            print(f"Error: User {user_id} not found")
            return False
        
        if resource_id not in self.resources:
            print(f"Error: Resource {resource_id} not found")
            return False
        
        if start_time >= end_time:
            print("Error: Start time must be before end time")
            return False
        
        if start_time < datetime.now():
            print("Error: Cannot book resources in the past")
            return False
        
        return True
    
    def _check_resource_availability(self, resource_id: str, start_time: datetime, end_time: datetime) -> bool:
        """Check if resource is available for the given time slot"""
        for booking in self.bookings.values():
            if (booking.resource_id == resource_id and 
                not (end_time <= booking.start_time or start_time >= booking.end_time)):
                return False
        return True
    
    def request_booking(self, user_id: str, resource_id: str, start_time: datetime, end_time: datetime) -> Optional[str]:
        """Submit a booking request"""
        if not self._validate_booking_request(user_id, resource_id, start_time, end_time):
            return None
        
        request_id = str(uuid.uuid4())
        user = self.users[user_id]
        request_timestamp = datetime.now()
        
        booking_request = BookingRequest(
            request_id=request_id,
            user_id=user_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            request_timestamp=request_timestamp,
            status="pending",
            priority_score=user.priority_score
        )
        
        self.booking_requests[request_id] = booking_request
        
        # Try immediate allocation
        if self._check_resource_availability(resource_id, start_time, end_time):
            # Allocate immediately
            booking_id = str(uuid.uuid4())
            booking = Booking(
                booking_id=booking_id,
                request_id=request_id,
                user_id=user_id,
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time,
                confirmed_at=datetime.now()
            )
            
            self.bookings[booking_id] = booking
            booking_request.status = "confirmed"
            
            resource_name = self.resources[resource_id].name
            print(f"✓ Booking confirmed! ID: {booking_id}")
            print(f"  Resource: {resource_name}")
            print(f"  Time: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')}")
            return booking_id
        else:
            # Add to priority queue and waiting list
            priority_item = (
                user.priority_score,
                request_timestamp.timestamp(),
                next(self.counter),
                request_id
            )
            heapq.heappush(self.priority_queue, priority_item)
            self.waiting_queues[resource_id].append(request_id)
            booking_request.status = "waitlisted"
            
            position = len(self.waiting_queues[resource_id])
            resource_name = self.resources[resource_id].name
            print(f"⏳ Request waitlisted for '{resource_name}'")
            print(f"  Position in queue: {position}")
            print(f"  Request ID: {request_id}")
            return request_id
    
    def cancel_booking(self, booking_id: str, user_id: str) -> bool:
        """Cancel a confirmed booking"""
        if booking_id not in self.bookings:
            print(f"Error: Booking {booking_id} not found")
            return False
        
        booking = self.bookings[booking_id]
        if booking.user_id != user_id:
            print("Error: You can only cancel your own bookings")
            return False
        
        # Remove the booking
        del self.bookings[booking_id]
        
        # Update request status
        if booking.request_id in self.booking_requests:
            self.booking_requests[booking.request_id].status = "cancelled"
        
        print(f"✓ Booking {booking_id} cancelled successfully")
        
        # Try to promote waiting requests
        self._process_waiting_queue(booking.resource_id)
        return True
    
    def _process_waiting_queue(self, resource_id: str):
        """Process waiting queue for a resource and try to allocate"""
        if resource_id not in self.waiting_queues:
            return
        
        waiting_queue = self.waiting_queues[resource_id]
        promoted_requests = []
        
        # Check each waiting request in priority order
        temp_queue = []
        while self.priority_queue:
            priority_item = heapq.heappop(self.priority_queue)
            request_id = priority_item[3]
            
            if request_id not in self.booking_requests:
                continue
                
            request = self.booking_requests[request_id]
            if (request.resource_id == resource_id and 
                request.status == "waitlisted" and
                self._check_resource_availability(resource_id, request.start_time, request.end_time)):
                
                # Allocate this request
                booking_id = str(uuid.uuid4())
                booking = Booking(
                    booking_id=booking_id,
                    request_id=request_id,
                    user_id=request.user_id,
                    resource_id=resource_id,
                    start_time=request.start_time,
                    end_time=request.end_time,
                    confirmed_at=datetime.now()
                )
                
                self.bookings[booking_id] = booking
                request.status = "confirmed"
                promoted_requests.append(request_id)
                
                # Remove from waiting queue
                if request_id in waiting_queue:
                    waiting_queue.remove(request_id)
                
                user_name = self.users[request.user_id].name
                resource_name = self.resources[resource_id].name
                print(f"🎉 Promoted from waitlist: {user_name} - {resource_name}")
                print(f"   Booking ID: {booking_id}")
            else:
                temp_queue.append(priority_item)
        
        # Restore non-processed items to priority queue
        for item in temp_queue:
            heapq.heappush(self.priority_queue, item)
    
    def list_users(self) -> None:
        """List all users in the system"""
        if not self.users:
            print("No users found")
            return
        
        print("\n=== USERS ===")
        print(f"{'ID':<10} {'Name':<20} {'Role':<10} {'Priority':<8} {'Email':<30}")
        print("-" * 80)
        
        for user in sorted(self.users.values(), key=lambda x: (x.priority_score, x.name)):
            print(f"{user.user_id:<10} {user.name:<20} {user.role:<10} {user.priority_score:<8} {user.email:<30}")
    
    def list_resources(self) -> None:
        """List all resources in the system"""
        if not self.resources:
            print("No resources found")
            return
        
        print("\n=== RESOURCES ===")
        print(f"{'ID':<8} {'Name':<20} {'Capacity':<8} {'Location':<25} {'Description':<30}")
        print("-" * 95)
        
        for resource in sorted(self.resources.values(), key=lambda x: x.name):
            print(f"{resource.resource_id:<8} {resource.name:<20} {resource.capacity:<8} {resource.location:<25} {resource.description:<30}")
    
    def list_allocations(self, resource_id: Optional[str] = None) -> None:
        """List current allocations"""
        bookings_to_show = []
        
        if resource_id:
            if resource_id not in self.resources:
                print(f"Error: Resource {resource_id} not found")
                return
            bookings_to_show = [b for b in self.bookings.values() if b.resource_id == resource_id]
            print(f"\n=== ALLOCATIONS FOR {self.resources[resource_id].name.upper()} ===")
        else:
            bookings_to_show = list(self.bookings.values())
            print("\n=== ALL CURRENT ALLOCATIONS ===")
        
        if not bookings_to_show:
            print("No current allocations")
            return
        
        print(f"{'Booking ID':<12} {'User':<20} {'Resource':<20} {'Start Time':<16} {'End Time':<16}")
        print("-" * 90)
        
        for booking in sorted(bookings_to_show, key=lambda x: x.start_time):
            user_name = self.users[booking.user_id].name
            resource_name = self.resources[booking.resource_id].name
            start_str = booking.start_time.strftime('%Y-%m-%d %H:%M')
            end_str = booking.end_time.strftime('%Y-%m-%d %H:%M')
            
            print(f"{booking.booking_id:<12} {user_name:<20} {resource_name:<20} {start_str:<16} {end_str:<16}")
    
    def list_waiting(self, resource_id: Optional[str] = None) -> None:
        """List waiting requests"""
        if resource_id:
            if resource_id not in self.resources:
                print(f"Error: Resource {resource_id} not found")
                return
            print(f"\n=== WAITING LIST FOR {self.resources[resource_id].name.upper()} ===")
            waiting_requests = [req for req in self.booking_requests.values() 
                              if req.resource_id == resource_id and req.status == "waitlisted"]
        else:
            print("\n=== ALL WAITING REQUESTS ===")
            waiting_requests = [req for req in self.booking_requests.values() if req.status == "waitlisted"]
        
        if not waiting_requests:
            print("No waiting requests")
            return
        
        print(f"{'Request ID':<12} {'User':<20} {'Resource':<20} {'Start Time':<16} {'Priority':<8}")
        print("-" * 85)
        
        # Sort by priority score, then by request timestamp
        waiting_requests.sort(key=lambda x: (x.priority_score, x.request_timestamp))
        
        for request in waiting_requests:
            user_name = self.users[request.user_id].name
            resource_name = self.resources[request.resource_id].name
            start_str = request.start_time.strftime('%Y-%m-%d %H:%M')
            
            print(f"{request.request_id:<12} {user_name:<20} {resource_name:<20} {start_str:<16} {request.priority_score:<8}")
    
    def get_user_bookings(self, user_id: str) -> None:
        """Get all bookings for a specific user"""
        if user_id not in self.users:
            print(f"Error: User {user_id} not found")
            return
        
        user_bookings = [b for b in self.bookings.values() if b.user_id == user_id]
        user_requests = [r for r in self.booking_requests.values() if r.user_id == user_id]
        
        user_name = self.users[user_id].name
        print(f"\n=== BOOKINGS FOR {user_name.upper()} ===")
        
        # Confirmed bookings
        if user_bookings:
            print("\nConfirmed Bookings:")
            print(f"{'Booking ID':<12} {'Resource':<20} {'Start Time':<16} {'End Time':<16}")
            print("-" * 70)
            
            for booking in sorted(user_bookings, key=lambda x: x.start_time):
                resource_name = self.resources[booking.resource_id].name
                start_str = booking.start_time.strftime('%Y-%m-%d %H:%M')
                end_str = booking.end_time.strftime('%Y-%m-%d %H:%M')
                print(f"{booking.booking_id:<12} {resource_name:<20} {start_str:<16} {end_str:<16}")
        
        # Waitlisted requests
        waitlisted = [r for r in user_requests if r.status == "waitlisted"]
        if waitlisted:
            print("\nWaitlisted Requests:")
            print(f"{'Request ID':<12} {'Resource':<20} {'Start Time':<16} {'Status':<12}")
            print("-" * 65)
            
            for request in sorted(waitlisted, key=lambda x: x.request_timestamp):
                resource_name = self.resources[request.resource_id].name
                start_str = request.start_time.strftime('%Y-%m-%d %H:%M')
                print(f"{request.request_id:<12} {resource_name:<20} {start_str:<16} {request.status:<12}")
        
        if not user_bookings and not waitlisted:
            print("No bookings or requests found")
    
    def save_state(self, filename: str = "campus_state.json") -> bool:
        """Save system state to JSON file"""
        try:
            state = {
                "users": {uid: asdict(user) for uid, user in self.users.items()},
                "resources": {rid: asdict(resource) for rid, resource in self.resources.items()},
                "bookings": {},
                "booking_requests": {},
                "waiting_queues": {rid: list(queue) for rid, queue in self.waiting_queues.items()},
                "saved_at": datetime.now().isoformat()
            }
            
            # Convert bookings with datetime serialization
            for bid, booking in self.bookings.items():
                booking_dict = asdict(booking)
                booking_dict["start_time"] = booking.start_time.isoformat()
                booking_dict["end_time"] = booking.end_time.isoformat()
                booking_dict["confirmed_at"] = booking.confirmed_at.isoformat()
                state["bookings"][bid] = booking_dict
            
            # Convert booking requests with datetime serialization
            for rid, request in self.booking_requests.items():
                request_dict = asdict(request)
                request_dict["start_time"] = request.start_time.isoformat()
                request_dict["end_time"] = request.end_time.isoformat()
                request_dict["request_timestamp"] = request.request_timestamp.isoformat()
                state["booking_requests"][rid] = request_dict
            
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2)
            
            print(f"✓ System state saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
    
    def load_state(self, filename: str = "campus_state.json") -> bool:
        """Load system state from JSON file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            # Clear current state
            self.users.clear()
            self.resources.clear()
            self.bookings.clear()
            self.booking_requests.clear()
            self.waiting_queues.clear()
            self.priority_queue.clear()
            
            # Load users
            for uid, user_data in state.get("users", {}).items():
                self.users[uid] = User(**user_data)
            
            # Load resources
            for rid, resource_data in state.get("resources", {}).items():
                self.resources[rid] = Resource(**resource_data)
                self.waiting_queues[rid] = deque()
            
            # Load bookings
            for bid, booking_data in state.get("bookings", {}).items():
                booking_data["start_time"] = datetime.fromisoformat(booking_data["start_time"])
                booking_data["end_time"] = datetime.fromisoformat(booking_data["end_time"])
                booking_data["confirmed_at"] = datetime.fromisoformat(booking_data["confirmed_at"])
                self.bookings[bid] = Booking(**booking_data)
            
            # Load booking requests
            for rid, request_data in state.get("booking_requests", {}).items():
                request_data["start_time"] = datetime.fromisoformat(request_data["start_time"])
                request_data["end_time"] = datetime.fromisoformat(request_data["end_time"])
                request_data["request_timestamp"] = datetime.fromisoformat(request_data["request_timestamp"])
                request = BookingRequest(**request_data)
                self.booking_requests[rid] = request
                
                # Rebuild priority queue for waitlisted requests
                if request.status == "waitlisted":
                    priority_item = (
                        request.priority_score,
                        request.request_timestamp.timestamp(),
                        next(self.counter),
                        rid
                    )
                    heapq.heappush(self.priority_queue, priority_item)
            
            # Load waiting queues
            for rid, queue_list in state.get("waiting_queues", {}).items():
                if rid in self.waiting_queues:
                    self.waiting_queues[rid] = deque(queue_list)
            
            print(f"✓ System state loaded from {filename}")
            print(f"  Loaded: {len(self.users)} users, {len(self.resources)} resources, {len(self.bookings)} bookings")
            return True
            
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading state: {e}")
            return False

def parse_datetime(date_str: str) -> Optional[datetime]:
    """Parse datetime string in ISO format"""
    try:
        return datetime.fromisoformat(date_str.replace('T', ' '))
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return None

def main():
    """Main CLI interface"""
    system = SmartCampusSystem()
    
    print("🎓 Smart Campus Resource Allocation System")
    print("=" * 50)
    print("System initialized with sample users and resources")
    
    while True:
        print("\n" + "=" * 50)
        print("COMMANDS:")
        print("1. add_user <user_id> <name> <role> <email>")
        print("2. add_resource <resource_id> <name> <capacity> <location> <description>")
        print("3. request_booking <user_id> <resource_id> <start_time> <end_time>")
        print("4. cancel_booking <booking_id> <user_id>")
        print("5. list_users")
        print("6. list_resources")
        print("7. list_allocations [resource_id]")
        print("8. list_waiting [resource_id]")
        print("9. user_bookings <user_id>")
        print("10. save_state [filename]")
        print("11. load_state [filename]")
        print("12. help")
        print("13. exit")
        print("\nTime format: YYYY-MM-DD HH:MM (e.g., 2026-02-01 14:00)")
        
        try:
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "add_user":
                if len(command) < 5:
                    print("Usage: add_user <user_id> <name> <role> <email>")
                    continue
                user_id, name, role, email = command[1], command[2], command[3], command[4]
                system.add_user(user_id, name, role, email)
            
            elif cmd == "add_resource":
                if len(command) < 6:
                    print("Usage: add_resource <resource_id> <name> <capacity> <location> <description>")
                    continue
                try:
                    resource_id = command[1]
                    name = command[2]
                    capacity = int(command[3])
                    location = command[4]
                    description = " ".join(command[5:])
                    system.add_resource(resource_id, name, capacity, location, description)
                except ValueError:
                    print("Error: Capacity must be a number")
            
            elif cmd == "request_booking":
                if len(command) < 5:
                    print("Usage: request_booking <user_id> <resource_id> <start_time> <end_time>")
                    print("Time format: YYYY-MM-DD HH:MM")
                    continue
                
                user_id, resource_id = command[1], command[2]
                start_str = " ".join(command[3:5])
                end_str = " ".join(command[5:7]) if len(command) >= 7 else ""
                
                if not end_str:
                    print("Error: Please provide both start and end times")
                    continue
                
                start_time = parse_datetime(start_str)
                end_time = parse_datetime(end_str)
                
                if not start_time or not end_time:
                    print("Error: Invalid time format. Use YYYY-MM-DD HH:MM")
                    continue
                
                system.request_booking(user_id, resource_id, start_time, end_time)
            
            elif cmd == "cancel_booking":
                if len(command) < 3:
                    print("Usage: cancel_booking <booking_id> <user_id>")
                    continue
                booking_id, user_id = command[1], command[2]
                system.cancel_booking(booking_id, user_id)
            
            elif cmd == "list_users":
                system.list_users()
            
            elif cmd == "list_resources":
                system.list_resources()
            
            elif cmd == "list_allocations":
                resource_id = command[1] if len(command) > 1 else None
                system.list_allocations(resource_id)
            
            elif cmd == "list_waiting":
                resource_id = command[1] if len(command) > 1 else None
                system.list_waiting(resource_id)
            
            elif cmd == "user_bookings":
                if len(command) < 2:
                    print("Usage: user_bookings <user_id>")
                    continue
                user_id = command[1]
                system.get_user_bookings(user_id)
            
            elif cmd == "save_state":
                filename = command[1] if len(command) > 1 else "campus_state.json"
                system.save_state(filename)
            
            elif cmd == "load_state":
                filename = command[1] if len(command) > 1 else "campus_state.json"
                system.load_state(filename)
            
            elif cmd == "help":
                print("\n📖 HELP - Smart Campus Resource Allocation System")
                print("\nSample Commands:")
                print("• add_user user009 'John Doe' Student john.doe@student.university.edu")
                print("• add_resource res009 'Lab C' 25 'Building 3' 'New computer lab'")
                print("• request_booking user003 res001 '2026-02-01 14:00' '2026-02-01 16:00'")
                print("• cancel_booking <booking_id> user003")
                print("• list_allocations res001")
                print("• user_bookings user003")
                print("\nPriority System:")
                print("• Faculty (Priority 1) > Students (Priority 2)")
                print("• Ties broken by request timestamp")
                print("• Automatic waitlist promotion on cancellations")
                
            elif cmd == "exit":
                print("👋 Goodbye!")
                break
            
            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
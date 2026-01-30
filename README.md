# Smart Campus Resource Allocation System

A Python-based resource booking system that brings order to campus resource allocation with fair prioritization, conflict resolution, and efficient time slot management.

## 🎯 Overview

The Smart Campus Resource Allocation System addresses the common challenge of managing shared campus resources like computer labs, conference rooms, and equipment. It provides:

- **Role-based Priority**: Faculty bookings can preempt student bookings when conflicts arise
- **Fair Queuing**: Same-priority users are handled in request order
- **Conflict Resolution**: Automatic detection and handling of scheduling conflicts
- **Waitlist Management**: Automatic promotion when resources become available
- **Multi-resource Support**: Manage multiple resources independently
- **Web Interface**: Modern, responsive web UI for easy management
- **Persistent Storage**: Save and restore system state

## 🌐 Web Interface

### Quick Start (Recommended)
```bash
python start_web.py
```
This will start the web server and automatically open your browser to http://localhost:5000

### Manual Start
```bash
python app.py
```
Then visit http://localhost:5000 in your browser

### Load Demo Data
Visit http://localhost:5000/demo_data to populate the system with sample users, resources, and bookings.

## 🏗️ Architecture

```
├── app.py           # Flask web application
├── start_web.py     # Quick start script with auto-browser
├── main.py          # Interactive CLI interface
├── models.py        # Data models (User, Resource, Booking, BookingRequest)
├── scheduler.py     # Core scheduling logic and algorithms
├── storage.py       # State persistence (save/load)
├── utils.py         # Utility functions (time parsing, overlap detection)
├── tests.py         # Comprehensive test suite
├── demo.py          # Interactive demonstration
├── templates/       # HTML templates for web interface
│   ├── base.html    # Base template with navigation
│   ├── index.html   # Dashboard with bookings and stats
│   ├── book.html    # Booking request form
│   ├── users.html   # User management
│   └── resources.html # Resource management
└── README.md        # This file
```

## 🚀 Quick Start Options

### 🌐 Web Interface (Recommended)
```bash
python start_web.py
```
- Modern, responsive web UI
- Real-time dashboard
- Easy booking management
- Visual conflict resolution
- Auto-loads demo data option

### 🖥️ Interactive Demo
```bash
python demo.py
```
- Comprehensive feature demonstration
- Pre-configured scenarios
- Shows priority system in action

### 🧪 Run Tests
```bash
python tests.py
```
- Complete test suite
- Validates all functionality
- Shows system behavior

### 💻 Command Line Interface
```bash
python main.py
```
- Interactive CLI commands
- Direct system access
- Good for automation

## 📋 Features

### ✅ User Management
- **Faculty**: Priority 0 (highest priority)
- **Students**: Priority 1 (lower priority)
- Unique user IDs with role-based permissions

### ✅ Resource Management
- Multiple resource types (labs, rooms, equipment)
- Independent scheduling per resource
- Capacity tracking (extensible)

### ✅ Smart Scheduling
- **Priority Preemption**: Faculty can preempt student bookings
- **Conflict Detection**: Automatic overlap detection
- **Fair Queuing**: FIFO for same-priority requests
- **Waitlist Management**: Automatic promotion when slots open

### ✅ Web Interface Features
- **Dashboard**: Real-time system overview with statistics
- **Booking Management**: Easy request and cancellation
- **User Management**: Add faculty and students
- **Resource Management**: Add and monitor facilities
- **Visual Feedback**: Color-coded priorities and status
- **Responsive Design**: Works on desktop and mobile

### ✅ Booking Lifecycle
1. **Request**: User submits booking request via web or CLI
2. **Prioritization**: Requests sorted by priority + timestamp
3. **Allocation**: Check conflicts, preempt if necessary
4. **Confirmation**: Immediate feedback to user
5. **Waitlisting**: Queue lower-priority conflicting requests

## 🔧 API Usage

### Basic Operations

```python
from scheduler import Scheduler
from datetime import datetime, timedelta

# Initialize system
scheduler = Scheduler()

# Add users
faculty_id = scheduler.add_user("Dr. Smith", "Faculty")
student_id = scheduler.add_user("Alice", "Student")

# Add resources
lab_id = scheduler.add_resource("Computer Lab A")

# Make bookings
start_time = datetime.now() + timedelta(hours=1)
end_time = start_time + timedelta(hours=2)

result = scheduler.request_booking(student_id, lab_id, start_time, end_time)
print(result)  # "CONFIRMED: booking-id" or "WAITLISTED: request-id"

# Cancel booking
scheduler.cancel_booking(booking_id)
```

### Priority System Example

```python
# Student books first
student_result = scheduler.request_booking(student_id, lab_id, start, end)
# Result: "CONFIRMED: abc-123"

# Faculty requests same slot - preempts student
faculty_result = scheduler.request_booking(faculty_id, lab_id, start, end)
# Result: "CONFIRMED: def-456 (preempted: Alice)"

# Student is automatically moved to waitlist
```

## 🧪 Testing

The system includes comprehensive tests covering:

- **Basic Operations**: User/resource creation, booking, cancellation
- **Priority System**: Faculty preemption of student bookings
- **Conflict Resolution**: Overlap detection and waitlist management
- **Edge Cases**: Invalid inputs, boundary conditions
- **System State**: Verification of internal data structures

Run tests:
```bash
python tests.py
```

## 💾 Data Persistence

Save and restore system state:

```python
from storage import save_state, load_state

# Save current state
save_state(scheduler, "campus_state.json")

# Load previous state
new_scheduler = Scheduler()
load_state(new_scheduler, "campus_state.json")
```

The web interface automatically saves state after each operation.

## 🎮 Interactive CLI

The system provides a user-friendly command-line interface:

```bash
python main.py
```

Available commands:
- `add_user`: Create new faculty or student user
- `add_resource`: Add new bookable resource
- `book`: Request a booking (with conflict resolution)
- `cancel`: Cancel existing booking
- `exit`: Quit the system

## 🏛️ Real-World Applications

This system design mirrors production resource allocation systems:

- **University Labs**: Computer labs, research facilities
- **Corporate Resources**: Meeting rooms, equipment
- **Healthcare**: Operating rooms, medical equipment
- **Shared Workspaces**: Hot desks, conference rooms

## 🔮 Extensibility

The modular design supports easy extensions:

- **Capacity Management**: Multi-user resources
- **Recurring Bookings**: Weekly/monthly patterns
- **Advanced Policies**: Department quotas, time limits
- **Notifications**: Email/SMS alerts
- **REST API**: JSON API endpoints
- **Analytics**: Usage reports and optimization

## 🧠 Algorithm Details

### Priority Queue Implementation
- Uses Python's `heapq` for O(log n) insertion/extraction
- Composite sort key: `(priority, request_time, user_id, resource_id)`
- Ensures deterministic ordering for fair processing

### Conflict Resolution
1. **Detection**: Check time overlap with existing bookings
2. **Preemption**: Higher priority users can displace lower priority
3. **Waitlisting**: Conflicting requests queued for later processing
4. **Promotion**: Automatic advancement when resources free up

### Time Complexity
- **Booking Request**: O(log n + m) where n = queue size, m = existing bookings
- **Cancellation**: O(m + w) where m = bookings, w = waitlist size
- **Waitlist Promotion**: O(w × m) for complete waitlist processing

## 📊 System Metrics

The demo shows typical system behavior:
- **Faculty Preemption**: ~100% success rate for priority conflicts
- **Waitlist Efficiency**: Automatic promotion on cancellation
- **Resource Utilization**: Clear visibility into booking patterns
- **User Experience**: Immediate feedback on all operations

## 🛠️ Requirements

- Python 3.7+
- Flask (for web interface)
- Modern web browser (for UI)

Install dependencies:
```bash
pip install flask
```

---

*Built with Python 3.7+ • Flask Web Framework • Bootstrap UI • Production-ready architecture*
#!/usr/bin/env python3
"""
Smart Campus System - Interactive Demo
Demonstrates key features with realistic scenarios
"""

from datetime import datetime, timedelta
from smart_campus import SmartCampusSystem

def demo_priority_system():
    """Demonstrate priority-based scheduling"""
    print("\n" + "="*60)
    print("🎯 DEMO: Priority-Based Scheduling")
    print("="*60)
    
    system = SmartCampusSystem()
    
    # Clear sample data for clean demo
    system.users.clear()
    system.resources.clear()
    system.bookings.clear()
    system.booking_requests.clear()
    system.waiting_queues.clear()
    system.priority_queue.clear()
    
    # Add demo users
    system.add_user("prof1", "Dr. Emily Chen", "Faculty", "emily.chen@university.edu")
    system.add_user("student1", "Alex Johnson", "Student", "alex.johnson@student.university.edu")
    system.add_user("student2", "Maria Garcia", "Student", "maria.garcia@student.university.edu")
    
    # Add demo resource
    system.add_resource("lab1", "AI Research Lab", 15, "Tech Building Floor 3", "Advanced AI/ML laboratory")
    
    print("\n📅 Scenario: Multiple users want the same time slot")
    
    # Same time slot for all requests
    start_time = datetime(2026, 2, 3, 14, 0)  # Monday 2 PM
    end_time = datetime(2026, 2, 3, 16, 0)    # Monday 4 PM
    
    print(f"Requested time: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Student requests first
    print("\n1️⃣ Student Alex requests the lab...")
    alex_request = system.request_booking("student1", "lab1", start_time, end_time)
    
    # Another student requests same slot
    print("\n2️⃣ Student Maria requests the same slot...")
    maria_request = system.request_booking("student2", "lab1", start_time, end_time)
    
    # Faculty requests same slot
    print("\n3️⃣ Faculty Dr. Chen requests the same slot...")
    prof_request = system.request_booking("prof1", "lab1", start_time, end_time)
    
    print("\n📊 Current Status:")
    system.list_allocations()
    system.list_waiting()
    
    print("\n🔄 Now Dr. Chen (Faculty) cancels another booking to free up the slot...")
    # Find Alex's booking and cancel it to demonstrate promotion
    alex_booking = next((b for b in system.bookings.values() if b.user_id == "student1"), None)
    if alex_booking:
        system.cancel_booking(alex_booking.booking_id, "student1")
    
    print("\n📊 After cancellation - Notice automatic waitlist promotion:")
    system.list_allocations()
    system.list_waiting()

def demo_conflict_resolution():
    """Demonstrate overlap detection and conflict resolution"""
    print("\n" + "="*60)
    print("⚡ DEMO: Conflict Resolution & Overlap Detection")
    print("="*60)
    
    system = SmartCampusSystem()
    
    # Use existing sample data
    print("\n📅 Scenario: Overlapping booking requests")
    
    base_date = datetime(2026, 2, 5, 10, 0)  # Wednesday 10 AM
    
    # Create a series of overlapping requests
    bookings = [
        ("user003", "res001", base_date, base_date + timedelta(hours=2)),  # 10-12
        ("user004", "res001", base_date + timedelta(hours=1), base_date + timedelta(hours=3)),  # 11-13 (overlap)
        ("user001", "res001", base_date + timedelta(hours=1, minutes=30), base_date + timedelta(hours=3, minutes=30)),  # 11:30-13:30 (overlap)
        ("user005", "res001", base_date + timedelta(hours=3), base_date + timedelta(hours=5)),  # 13-15 (no overlap)
    ]
    
    print("Requesting overlapping time slots:")
    for i, (user_id, resource_id, start, end) in enumerate(bookings, 1):
        user_name = system.users[user_id].name
        print(f"\n{i}️⃣ {user_name} requests {start.strftime('%H:%M')}-{end.strftime('%H:%M')}")
        result = system.request_booking(user_id, resource_id, start, end)
        if result:
            status = system.booking_requests[result].status
            print(f"   Result: {status}")
    
    print("\n📊 Final allocation results:")
    system.list_allocations("res001")
    system.list_waiting("res001")

def demo_realistic_campus_day():
    """Demonstrate a realistic campus day with multiple bookings"""
    print("\n" + "="*60)
    print("🏫 DEMO: Realistic Campus Day Simulation")
    print("="*60)
    
    system = SmartCampusSystem()
    
    print("\n📅 Simulating a busy Tuesday with multiple resources and users")
    
    # Create realistic booking schedule
    tuesday = datetime(2026, 2, 4, 8, 0)  # Tuesday 8 AM
    
    # Morning classes and meetings
    morning_bookings = [
        ("user001", "res002", tuesday + timedelta(hours=1), tuesday + timedelta(hours=2, minutes=30)),  # 9-10:30 Seminar
        ("user002", "res001", tuesday + timedelta(hours=2), tuesday + timedelta(hours=4)),  # 10-12 Lab
        ("user005", "res003", tuesday + timedelta(hours=2, minutes=30), tuesday + timedelta(hours=3, minutes=30)),  # 10:30-11:30 Meeting
    ]
    
    # Afternoon sessions
    afternoon_bookings = [
        ("user008", "res006", tuesday + timedelta(hours=6), tuesday + timedelta(hours=8)),  # 2-4 PM Auditorium
        ("user003", "res004", tuesday + timedelta(hours=6, minutes=30), tuesday + timedelta(hours=8, minutes=30)),  # 2:30-4:30 Physics Lab
        ("user004", "res001", tuesday + timedelta(hours=7), tuesday + timedelta(hours=9)),  # 3-5 PM Computer Lab
    ]
    
    all_bookings = morning_bookings + afternoon_bookings
    
    print("\n🌅 Morning Session Bookings:")
    for user_id, resource_id, start, end in morning_bookings:
        user_name = system.users[user_id].name
        resource_name = system.resources[resource_id].name
        print(f"   {user_name} → {resource_name} ({start.strftime('%H:%M')}-{end.strftime('%H:%M')})")
        system.request_booking(user_id, resource_id, start, end)
    
    print("\n🌆 Afternoon Session Bookings:")
    for user_id, resource_id, start, end in afternoon_bookings:
        user_name = system.users[user_id].name
        resource_name = system.resources[resource_id].name
        print(f"   {user_name} → {resource_name} ({start.strftime('%H:%M')}-{end.strftime('%H:%M')})")
        system.request_booking(user_id, resource_id, start, end)
    
    print("\n📊 Complete Day Schedule:")
    system.list_allocations()
    
    # Demonstrate user-specific view
    print("\n👤 Individual User Schedule (Dr. Sarah Johnson):")
    system.get_user_bookings("user001")

def demo_state_persistence():
    """Demonstrate save/load functionality"""
    print("\n" + "="*60)
    print("💾 DEMO: State Persistence")
    print("="*60)
    
    system = SmartCampusSystem()
    
    # Create some bookings
    tomorrow = datetime.now() + timedelta(days=1)
    system.request_booking("user001", "res001", tomorrow, tomorrow + timedelta(hours=2))
    system.request_booking("user003", "res002", tomorrow + timedelta(hours=1), tomorrow + timedelta(hours=3))
    
    print(f"\n📊 Current system state:")
    print(f"   Users: {len(system.users)}")
    print(f"   Resources: {len(system.resources)}")
    print(f"   Active bookings: {len(system.bookings)}")
    print(f"   Waiting requests: {sum(len(q) for q in system.waiting_queues.values())}")
    
    # Save state
    print("\n💾 Saving system state...")
    system.save_state("demo_backup.json")
    
    # Simulate system restart by clearing data
    original_counts = (len(system.users), len(system.resources), len(system.bookings))
    system.users.clear()
    system.resources.clear()
    system.bookings.clear()
    
    print(f"\n🔄 After simulated restart:")
    print(f"   Users: {len(system.users)}")
    print(f"   Resources: {len(system.resources)}")
    print(f"   Active bookings: {len(system.bookings)}")
    
    # Load state
    print("\n📂 Loading saved state...")
    system.load_state("demo_backup.json")
    
    print(f"\n✅ After loading:")
    print(f"   Users: {len(system.users)}")
    print(f"   Resources: {len(system.resources)}")
    print(f"   Active bookings: {len(system.bookings)}")
    
    print("\n🎯 State persistence successful!")

def main():
    """Run all demonstrations"""
    print("🎓 Smart Campus Resource Allocation System")
    print("🎬 Interactive Feature Demonstration")
    print("=" * 70)
    
    try:
        demo_priority_system()
        input("\nPress Enter to continue to next demo...")
        
        demo_conflict_resolution()
        input("\nPress Enter to continue to next demo...")
        
        demo_realistic_campus_day()
        input("\nPress Enter to continue to next demo...")
        
        demo_state_persistence()
        
        print("\n" + "="*70)
        print("🎉 All demonstrations completed successfully!")
        print("💡 Try running 'python smart_campus.py' for interactive CLI")
        print("🧪 Run 'python test_smart_campus.py' for comprehensive tests")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()
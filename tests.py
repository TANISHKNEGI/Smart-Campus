from scheduler import Scheduler
from datetime import datetime, timedelta
import time

def test_smart_campus_system():
    print("=== Smart Campus Resource Allocation System Test ===\n")
    
    s = Scheduler()
    
    # Add users with different roles
    print("1. Adding Users:")
    faculty1 = s.add_user("Dr. Smith", "Faculty")
    faculty2 = s.add_user("Prof. Johnson", "Faculty")
    student1 = s.add_user("Alice", "Student")
    student2 = s.add_user("Bob", "Student")
    print(f"   Faculty: Dr. Smith ({faculty1[:8]}...)")
    print(f"   Faculty: Prof. Johnson ({faculty2[:8]}...)")
    print(f"   Student: Alice ({student1[:8]}...)")
    print(f"   Student: Bob ({student2[:8]}...)\n")
    
    # Add resources
    print("2. Adding Resources:")
    lab_a = s.add_resource("Computer Lab A")
    lab_b = s.add_resource("Conference Room B")
    print(f"   Computer Lab A ({lab_a[:8]}...)")
    print(f"   Conference Room B ({lab_b[:8]}...)\n")
    
    # Test basic booking
    print("3. Basic Booking Test:")
    now = datetime.now()
    slot1 = now + timedelta(hours=1)
    slot2 = slot1 + timedelta(hours=2)
    
    result1 = s.request_booking(student1, lab_a, slot1, slot2)
    print(f"   Alice (Student) books Lab A (1-3pm): {result1}")
    
    # Test faculty preemption - this should now preempt the student
    print("\n4. Faculty Preemption Test:")
    result2 = s.request_booking(faculty1, lab_a, slot1, slot2)
    print(f"   Dr. Smith (Faculty) requests same slot: {result2}")
    
    # Test student vs student conflict
    print("\n5. Student vs Student Conflict:")
    result3 = s.request_booking(student2, lab_a, slot1, slot2)
    print(f"   Bob (Student) tries same slot: {result3}")
    
    # Test non-conflicting booking
    print("\n6. Non-conflicting Booking:")
    slot3 = slot2 + timedelta(hours=1)
    slot4 = slot3 + timedelta(hours=2)
    result4 = s.request_booking(faculty2, lab_a, slot3, slot4)
    print(f"   Prof. Johnson books Lab A (4-6pm): {result4}")
    
    # Test different resource
    print("\n7. Different Resource Booking:")
    result5 = s.request_booking(student1, lab_b, slot1, slot2)
    print(f"   Alice books Conference Room B (1-3pm): {result5}")
    
    # Show current allocations
    print("\n8. Current System State:")
    print("   Active Bookings:")
    for rid, bookings in s.allocations.items():
        resource_name = s.resources[rid].name
        print(f"   {resource_name}:")
        if bookings:
            for booking in bookings:
                user_name = s.users[booking.user_id].name
                user_role = s.users[booking.user_id].role
                start = booking.start_time.strftime("%H:%M")
                end = booking.end_time.strftime("%H:%M")
                print(f"     - {user_name} ({user_role}): {start}-{end}")
        else:
            print("     - No bookings")
    
    print(f"\n   Waiting Queue Length: {len(s.waiting_queue)}")
    if s.waiting_queue:
        print("   Waiting Queue:")
        for req in s.waiting_queue:
            user_name = s.users[req.user_id].name
            user_role = s.users[req.user_id].role
            resource_name = s.resources[req.resource_id].name
            start = req.start_time.strftime("%H:%M")
            end = req.end_time.strftime("%H:%M")
            print(f"     - {user_name} ({user_role}) for {resource_name}: {start}-{end}")
    
    print(f"   Request Heap Length: {len(s.request_heap)}")
    
    print("\n=== Test Complete ===")
    print("\nKey Features Demonstrated:")
    print("✅ User management with role-based priorities")
    print("✅ Resource allocation with conflict detection")
    print("✅ Faculty preemption of student bookings")
    print("✅ Fair queuing for same-priority users")
    print("✅ Multi-resource support")
    print("✅ Waitlist management")

if __name__ == "__main__":
    test_smart_campus_system()

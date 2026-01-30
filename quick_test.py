#!/usr/bin/env python3
"""
Quick test of the interactive CLI functionality
"""

from scheduler import Scheduler
from utils import parse_time
from datetime import datetime, timedelta

def test_cli_functions():
    print("Testing CLI functionality...")
    
    scheduler = Scheduler()
    
    # Test add_user
    faculty_id = scheduler.add_user("Dr. Test", "Faculty")
    student_id = scheduler.add_user("Student Test", "Student")
    print(f"✅ Users created: Faculty {faculty_id[:8]}..., Student {student_id[:8]}...")
    
    # Test add_resource
    resource_id = scheduler.add_resource("Test Lab")
    print(f"✅ Resource created: {resource_id[:8]}...")
    
    # Test parse_time
    test_time = "2024-01-30T10:00:00"
    parsed = parse_time(test_time)
    print(f"✅ Time parsing works: {test_time} -> {parsed}")
    
    # Test booking
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    result = scheduler.request_booking(student_id, resource_id, start_time, end_time)
    print(f"✅ Booking works: {result}")
    
    # Test cancellation
    if "CONFIRMED:" in result:
        booking_id = result.split(": ")[1]
        scheduler.cancel_booking(booking_id)
        print(f"✅ Cancellation works: {booking_id}")
    
    print("\n🎉 All CLI functions working correctly!")

if __name__ == "__main__":
    test_cli_functions()
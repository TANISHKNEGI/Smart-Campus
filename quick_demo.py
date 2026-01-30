#!/usr/bin/env python3
"""
Quick Demo of Smart Campus System
Shows key features with sample data
"""

from smart_campus import SmartCampusSystem
from datetime import datetime, timedelta

def main():
    print("🎓 Smart Campus Resource Allocation System - Demo")
    print("=" * 60)
    
    # Create system (already has sample data)
    system = SmartCampusSystem()
    
    print("\n📊 SAMPLE USERS:")
    system.list_users()
    
    print("\n📊 SAMPLE RESOURCES:")
    system.list_resources()
    
    print("\n🎯 TESTING PRIORITY-BASED SCHEDULING:")
    print("Scenario: Student vs Faculty requesting same time slot")
    
    # Test booking requests
    start_time = datetime(2026, 2, 1, 14, 0)
    end_time = datetime(2026, 2, 1, 16, 0)
    
    print(f"\nTime slot: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n1️⃣ Student Alice requests Computer Lab A...")
    result1 = system.request_booking("user003", "res001", start_time, end_time)
    
    print("\n2️⃣ Faculty Dr. Sarah requests same slot...")
    result2 = system.request_booking("user001", "res001", start_time, end_time)
    
    print("\n📊 CURRENT ALLOCATIONS:")
    system.list_allocations("res001")
    
    print("\n📊 WAITING LIST:")
    system.list_waiting("res001")
    
    print("\n🔄 TESTING WAITLIST PROMOTION:")
    print("Cancelling Alice's booking to promote faculty...")
    
    # Find Alice's booking
    alice_booking = None
    for booking in system.bookings.values():
        if booking.user_id == "user003":
            alice_booking = booking
            break
    
    if alice_booking:
        system.cancel_booking(alice_booking.booking_id, "user003")
    
    print("\n📊 AFTER CANCELLATION:")
    system.list_allocations("res001")
    system.list_waiting("res001")
    
    print("\n👤 USER BOOKING HISTORY:")
    print("Dr. Sarah Johnson's bookings:")
    system.get_user_bookings("user001")
    
    print("\n✅ Demo completed successfully!")
    print("💡 Run 'python smart_campus.py' for interactive CLI")
    print("🧪 Run 'python test_smart_campus.py' for comprehensive tests")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Smart Campus Resource Allocation System - Demo Script
Demonstrates the key features with pre-configured scenarios
"""

from scheduler import Scheduler
from datetime import datetime, timedelta

def run_demo():
    print("🎓 Smart Campus Resource Allocation System - Demo")
    print("=" * 50)
    
    # Initialize system
    scheduler = Scheduler()
    
    # Setup users
    print("\n📋 Setting up users...")
    faculty1 = scheduler.add_user("Dr. Sarah Chen", "Faculty")
    faculty2 = scheduler.add_user("Prof. Michael Rodriguez", "Faculty")
    student1 = scheduler.add_user("Emma Thompson", "Student")
    student2 = scheduler.add_user("James Wilson", "Student")
    student3 = scheduler.add_user("Sophia Kim", "Student")
    
    print(f"   👩‍🏫 Dr. Sarah Chen (Faculty)")
    print(f"   👨‍🏫 Prof. Michael Rodriguez (Faculty)")
    print(f"   👩‍🎓 Emma Thompson (Student)")
    print(f"   👨‍🎓 James Wilson (Student)")
    print(f"   👩‍🎓 Sophia Kim (Student)")
    
    # Setup resources
    print("\n🏢 Setting up resources...")
    lab_a = scheduler.add_resource("Computer Lab A")
    lab_b = scheduler.add_resource("Physics Lab B")
    room_c = scheduler.add_resource("Conference Room C")
    
    print(f"   💻 Computer Lab A")
    print(f"   🔬 Physics Lab B")
    print(f"   🏛️ Conference Room C")
    
    # Demo scenarios
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    print("\n📅 Booking Scenarios:")
    print("-" * 30)
    
    # Scenario 1: Student books first
    print("\n1️⃣ Emma (Student) books Computer Lab A for 9-11 AM")
    result1 = scheduler.request_booking(student1, lab_a, base_time, base_time + timedelta(hours=2))
    print(f"   Result: {result1}")
    
    # Scenario 2: Faculty preempts student
    print("\n2️⃣ Dr. Chen (Faculty) needs the same slot - should preempt Emma")
    result2 = scheduler.request_booking(faculty1, lab_a, base_time, base_time + timedelta(hours=2))
    print(f"   Result: {result2}")
    
    # Scenario 3: Another student tries - should be waitlisted
    print("\n3️⃣ James (Student) tries the same slot - should be waitlisted")
    result3 = scheduler.request_booking(student2, lab_a, base_time, base_time + timedelta(hours=2))
    print(f"   Result: {result3}")
    
    # Scenario 4: Different time slot works
    print("\n4️⃣ Sophia (Student) books Computer Lab A for 2-4 PM")
    afternoon_slot = base_time + timedelta(hours=5)
    result4 = scheduler.request_booking(student3, lab_a, afternoon_slot, afternoon_slot + timedelta(hours=2))
    print(f"   Result: {result4}")
    
    # Scenario 5: Different resource
    print("\n5️⃣ Emma books Physics Lab B for 9-11 AM (different resource)")
    result5 = scheduler.request_booking(student1, lab_b, base_time, base_time + timedelta(hours=2))
    print(f"   Result: {result5}")
    
    # Show final state
    print("\n📊 Final System State:")
    print("-" * 30)
    
    for rid, bookings in scheduler.allocations.items():
        resource_name = scheduler.resources[rid].name
        print(f"\n🏛️ {resource_name}:")
        if bookings:
            for booking in sorted(bookings, key=lambda b: b.start_time):
                user = scheduler.users[booking.user_id]
                start_time = booking.start_time.strftime("%I:%M %p")
                end_time = booking.end_time.strftime("%I:%M %p")
                role_emoji = "👩‍🏫" if user.role == "Faculty" else "👩‍🎓"
                print(f"   {role_emoji} {user.name}: {start_time} - {end_time}")
        else:
            print("   📭 No bookings")
    
    if scheduler.waiting_queue:
        print(f"\n⏳ Waiting Queue ({len(scheduler.waiting_queue)} requests):")
        for req in scheduler.waiting_queue:
            user = scheduler.users[req.user_id]
            resource = scheduler.resources[req.resource_id]
            start_time = req.start_time.strftime("%I:%M %p")
            end_time = req.end_time.strftime("%I:%M %p")
            role_emoji = "👩‍🏫" if user.role == "Faculty" else "👩‍🎓"
            print(f"   {role_emoji} {user.name} for {resource.name}: {start_time} - {end_time}")
    
    print(f"\n✨ Demo complete! The system successfully:")
    print("   • Managed role-based priorities (Faculty > Student)")
    print("   • Handled resource conflicts with preemption")
    print("   • Maintained fair waitlists")
    print("   • Supported multiple resources")
    print("   • Provided clear feedback to users")

if __name__ == "__main__":
    run_demo()
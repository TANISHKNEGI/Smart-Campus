#!/usr/bin/env python3
"""
Test script for Smart Campus Resource Allocation System
Validates core scheduling logic, priority ordering, overlap detection, and waitlist promotion
"""

import unittest
from datetime import datetime, timedelta
from smart_campus import SmartCampusSystem, User, Resource, BookingRequest, Booking

class TestSmartCampusSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test system with clean state"""
        self.system = SmartCampusSystem()
        # Clear sample data for clean testing
        self.system.users.clear()
        self.system.resources.clear()
        self.system.bookings.clear()
        self.system.booking_requests.clear()
        self.system.waiting_queues.clear()
        self.system.priority_queue.clear()
        
        # Add test users
        self.system.add_user("faculty1", "Dr. Smith", "Faculty", "smith@university.edu")
        self.system.add_user("student1", "Alice Johnson", "Student", "alice@student.university.edu")
        self.system.add_user("student2", "Bob Wilson", "Student", "bob@student.university.edu")
        
        # Add test resource
        self.system.add_resource("lab1", "Test Lab", 20, "Building 1", "Test laboratory")
    
    def test_priority_ordering(self):
        """Test that faculty gets higher priority than students"""
        # Schedule overlapping requests
        start_time = datetime(2026, 2, 1, 14, 0)
        end_time = datetime(2026, 2, 1, 16, 0)
        
        # Student requests first
        student_request = self.system.request_booking("student1", "lab1", start_time, end_time)
        self.assertIsNotNone(student_request)
        
        # Faculty requests same slot (should be waitlisted but with higher priority)
        faculty_request = self.system.request_booking("faculty1", "lab1", start_time, end_time)
        self.assertIsNotNone(faculty_request)
        
        # Find the requests by user ID since return value might be booking ID
        faculty_req = None
        student_req = None
        for req in self.system.booking_requests.values():
            if req.user_id == "faculty1":
                faculty_req = req
            elif req.user_id == "student1":
                student_req = req
        
        self.assertIsNotNone(faculty_req)
        self.assertIsNotNone(student_req)
        self.assertEqual(faculty_req.priority_score, 1)  # Faculty priority
        self.assertEqual(student_req.priority_score, 2)  # Student priority
        self.assertEqual(faculty_req.status, "waitlisted")
        self.assertEqual(student_req.status, "confirmed")
    
    def test_overlap_detection(self):
        """Test booking overlap detection"""
        # First booking
        start1 = datetime(2026, 2, 1, 14, 0)
        end1 = datetime(2026, 2, 1, 16, 0)
        booking1 = self.system.request_booking("student1", "lab1", start1, end1)
        self.assertIsNotNone(booking1)
        
        # Overlapping booking (should be waitlisted)
        start2 = datetime(2026, 2, 1, 15, 0)
        end2 = datetime(2026, 2, 1, 17, 0)
        booking2 = self.system.request_booking("student2", "lab1", start2, end2)
        self.assertIsNotNone(booking2)
        
        # Check statuses
        req1 = next(req for req in self.system.booking_requests.values() if req.user_id == "student1")
        req2 = next(req for req in self.system.booking_requests.values() if req.user_id == "student2")
        
        self.assertEqual(req1.status, "confirmed")
        self.assertEqual(req2.status, "waitlisted")
        
        # Non-overlapping booking (should be confirmed)
        start3 = datetime(2026, 2, 1, 17, 0)
        end3 = datetime(2026, 2, 1, 19, 0)
        booking3 = self.system.request_booking("faculty1", "lab1", start3, end3)
        self.assertIsNotNone(booking3)
        
        req3 = next(req for req in self.system.booking_requests.values() if req.user_id == "faculty1")
        self.assertEqual(req3.status, "confirmed")
    
    def test_waitlist_promotion(self):
        """Test automatic waitlist promotion on cancellation"""
        # Create initial booking
        start1 = datetime(2026, 2, 1, 14, 0)
        end1 = datetime(2026, 2, 1, 16, 0)
        booking1_id = self.system.request_booking("student1", "lab1", start1, end1)
        
        # Create waitlisted request
        booking2_id = self.system.request_booking("faculty1", "lab1", start1, end1)
        
        # Find requests by user ID
        req1 = None
        req2 = None
        for req in self.system.booking_requests.values():
            if req.user_id == "student1":
                req1 = req
            elif req.user_id == "faculty1":
                req2 = req
        
        # Verify initial states
        self.assertIsNotNone(req1)
        self.assertIsNotNone(req2)
        self.assertEqual(req1.status, "confirmed")
        self.assertEqual(req2.status, "waitlisted")
        
        # Cancel first booking
        confirmed_booking = next(b for b in self.system.bookings.values() if b.user_id == "student1")
        success = self.system.cancel_booking(confirmed_booking.booking_id, "student1")
        self.assertTrue(success)
        
        # Check that faculty request was promoted
        req2_updated = None
        for req in self.system.booking_requests.values():
            if req.user_id == "faculty1":
                req2_updated = req
                break
        
        self.assertIsNotNone(req2_updated)
        self.assertEqual(req2_updated.status, "confirmed")
        
        # Verify new booking exists
        faculty_booking = next((b for b in self.system.bookings.values() if b.user_id == "faculty1"), None)
        self.assertIsNotNone(faculty_booking)
    
    def test_time_validation(self):
        """Test time validation logic"""
        # Test past time (should fail)
        past_time = datetime.now() - timedelta(hours=1)
        future_time = datetime.now() + timedelta(hours=1)
        result = self.system.request_booking("student1", "lab1", past_time, future_time)
        self.assertIsNone(result)
        
        # Test end before start (should fail)
        start = datetime(2026, 2, 1, 16, 0)
        end = datetime(2026, 2, 1, 14, 0)
        result = self.system.request_booking("student1", "lab1", start, end)
        self.assertIsNone(result)
        
        # Test valid times (should succeed)
        start = datetime(2026, 2, 1, 14, 0)
        end = datetime(2026, 2, 1, 16, 0)
        result = self.system.request_booking("student1", "lab1", start, end)
        self.assertIsNotNone(result)
    
    def test_user_resource_validation(self):
        """Test user and resource validation"""
        start = datetime(2026, 2, 1, 14, 0)
        end = datetime(2026, 2, 1, 16, 0)
        
        # Invalid user
        result = self.system.request_booking("invalid_user", "lab1", start, end)
        self.assertIsNone(result)
        
        # Invalid resource
        result = self.system.request_booking("student1", "invalid_resource", start, end)
        self.assertIsNone(result)
        
        # Valid user and resource
        result = self.system.request_booking("student1", "lab1", start, end)
        self.assertIsNotNone(result)
    
    def test_state_persistence(self):
        """Test save and load functionality"""
        # Create some bookings
        start = datetime(2026, 2, 1, 14, 0)
        end = datetime(2026, 2, 1, 16, 0)
        booking_id = self.system.request_booking("student1", "lab1", start, end)
        
        # Save state
        success = self.system.save_state("test_state.json")
        self.assertTrue(success)
        
        # Clear system
        original_bookings = len(self.system.bookings)
        original_requests = len(self.system.booking_requests)
        self.system.bookings.clear()
        self.system.booking_requests.clear()
        self.assertEqual(len(self.system.bookings), 0)
        
        # Load state
        success = self.system.load_state("test_state.json")
        self.assertTrue(success)
        
        # Verify restoration
        self.assertEqual(len(self.system.bookings), original_bookings)
        self.assertEqual(len(self.system.booking_requests), original_requests)
    
    def test_multiple_resources(self):
        """Test system with multiple resources"""
        # Add another resource
        self.system.add_resource("lab2", "Second Lab", 15, "Building 2", "Another lab")
        
        start = datetime(2026, 2, 1, 14, 0)
        end = datetime(2026, 2, 1, 16, 0)
        
        # Book both resources simultaneously
        booking1 = self.system.request_booking("student1", "lab1", start, end)
        booking2 = self.system.request_booking("student2", "lab2", start, end)
        
        self.assertIsNotNone(booking1)
        self.assertIsNotNone(booking2)
        
        # Find requests by user ID
        req1 = None
        req2 = None
        for req in self.system.booking_requests.values():
            if req.user_id == "student1":
                req1 = req
            elif req.user_id == "student2":
                req2 = req
        
        # Both should be confirmed (different resources)
        self.assertIsNotNone(req1)
        self.assertIsNotNone(req2)
        self.assertEqual(req1.status, "confirmed")
        self.assertEqual(req2.status, "confirmed")

def run_performance_test():
    """Test system performance with many requests"""
    print("\n🚀 Running Performance Test...")
    
    system = SmartCampusSystem()
    
    # Add many users
    for i in range(100):
        role = "Faculty" if i % 10 == 0 else "Student"
        system.add_user(f"user{i:03d}", f"User {i}", role, f"user{i}@university.edu")
    
    # Add resources
    for i in range(10):
        system.add_resource(f"res{i:03d}", f"Resource {i}", 20, f"Building {i}", f"Resource {i}")
    
    # Generate many booking requests
    import time
    start_time = time.time()
    
    base_datetime = datetime(2026, 2, 1, 9, 0)
    successful_bookings = 0
    
    for i in range(1000):
        user_id = f"user{i % 100:03d}"
        resource_id = f"res{i % 10:03d}"
        slot_start = base_datetime + timedelta(hours=i % 24, minutes=(i % 4) * 15)
        slot_end = slot_start + timedelta(hours=1)
        
        result = system.request_booking(user_id, resource_id, slot_start, slot_end)
        if result:
            successful_bookings += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Processed 1000 requests in {duration:.2f}ms")
    print(f"✓ {successful_bookings} successful bookings")
    print(f"✓ {len(system.bookings)} confirmed bookings")
    print(f"✓ {sum(len(q) for q in system.waiting_queues.values())} waiting requests")
    
    # Test heap operations performance
    print(f"✓ Priority queue size: {len(system.priority_queue)}")
    print("✓ Performance test completed successfully")

if __name__ == "__main__":
    print("🧪 Smart Campus System - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()
    
    print("\n✅ All tests completed!")
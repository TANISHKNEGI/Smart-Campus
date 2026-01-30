from scheduler import Scheduler
from utils import parse_time

scheduler = Scheduler()

print("Smart Campus Resource Allocation System")

while True:
    cmd = input("\nCommand (add_user, add_resource, book, cancel, exit): ")

    try:
        if cmd == "add_user":
            name = input("Name: ")
            role = input("Role (Faculty/Student): ")
            uid = scheduler.add_user(name, role)
            print("User ID:", uid)

        elif cmd == "add_resource":
            name = input("Resource name: ")
            rid = scheduler.add_resource(name)
            print("Resource ID:", rid)

        elif cmd == "book":
            uid = input("User ID: ")
            rid = input("Resource ID: ")
            start = parse_time(input("Start (ISO): "))
            end = parse_time(input("End (ISO): "))
            result = scheduler.request_booking(uid, rid, start, end)
            print(result)

        elif cmd == "cancel":
            bid = input("Booking ID: ")
            scheduler.cancel_booking(bid)
            print("Cancelled")

        elif cmd == "exit":
            break

    except Exception as e:
        print("Error:", e)

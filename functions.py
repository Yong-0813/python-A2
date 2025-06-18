# functions.py
import os
import random
from event import Event
from ticket import Ticket
from bill import Bill

DATA_FOLDER = "assignment2"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def get_path(filename):
    return os.path.join(DATA_FOLDER, filename)

def load_events():
    events = {}
    if not os.path.exists(get_path("events.txt")): return events
    with open(get_path("events.txt")) as f:
        for line in f:
            eid, name, date, venue, ttype, price, quota = line.strip().split(',')
            if eid not in events:
                events[eid] = Event(eid, name, date, venue)
            events[eid].add_ticket_type(ttype, float(price), int(quota))
    return events

def save_event(event):
    with open(get_path("events.txt"), "a") as f:
        for ttype, info in event.ticket_types.items():
            f.write(f"{event.event_id},{event.name},{event.date},{event.venue},{ttype},{info['price']},{info['quota']}\n")

def functionMenu():
    return {
        "1": "Add New Event",
        "2": "Book Ticket",
        "3": "Check-In Ticket",
        "4": "Show All Bookings",
        "5": "Exit"
    }

def get_next_booking_id():
    if not os.path.exists(get_path("bookings.txt")): return "B001"
    with open(get_path("bookings.txt")) as f:
        lines = f.readlines()
        if not lines: return "B001"
        last = int(lines[-1].split(',')[0][1:]) + 1
        return f"B{str(last).zfill(3)}"

def get_remaining_quota(event_id):
    sold = {}
    if os.path.exists(get_path("tickets.txt")):
        with open(get_path("tickets.txt")) as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[2] == event_id:
                    sold[parts[3]] = sold.get(parts[3], 0) + 1
    return sold

def generate_ticket_id(event_id, existing):
    while True:
        tid = f"{event_id}-{random.randint(100000,999999)}"
        if tid not in existing:
            return tid

def book_ticket():
    events = load_events()
    if not events:
        print("No events available.")
        return
    for eid, e in events.items():
        print(f"[{eid}] {e.name} - {e.date} at {e.venue}")
    eid = input("Enter Event ID: ").strip()
    if eid not in events:
        print("Invalid Event ID.")
        return
    event = events[eid]
    remaining = get_remaining_quota(eid)
    event.display_ticket_types(remaining)
    ttype = input("Enter Ticket Type: ").strip()
    if ttype not in event.ticket_types:
        print("Invalid ticket type.")
        return
    quota = event.ticket_types[ttype]['quota'] - remaining.get(ttype, 0)
    qty = int(input("Enter Quantity: "))
    if qty > quota:
        print("Not enough tickets.")
        return
    name = input("Enter Buyer Name: ").strip()
    ic = input("Enter IC/Passport No: ").strip()
    bid = get_next_booking_id()
    price = event.ticket_types[ttype]['price']
    bill = Bill(bid, name, ic, event, ttype, qty, price)
    existing_ids = set()
    if os.path.exists(get_path("tickets.txt")):
        with open(get_path("tickets.txt")) as f:
            for line in f:
                existing_ids.add(line.split(',')[0])
    with open(get_path("tickets.txt"), "a") as ft:
        for _ in range(qty):
            tid = generate_ticket_id(eid, existing_ids)
            ticket = Ticket(tid, bid, eid, ttype, name, ic)
            existing_ids.add(tid)
            bill.add_ticket(ticket)
            ft.write(ticket.to_line())
    with open(get_path("bookings.txt"), "a") as fb:
        fb.write(f"{bid},{name},{ic},{eid},{ttype},{qty},{bill.date},{bill.total_charge():.2f}\n")
    bill.print_invoice()

def check_in_ticket():
    tid = input("Enter Ticket ID: ").strip()
    updated = []
    found = False
    if not os.path.exists(get_path("tickets.txt")): return print("No ticket records.")
    with open(get_path("tickets.txt")) as f:
        for line in f:
            if line.startswith(tid + ","):
                found = True
                parts = line.strip().split(',')
                if parts[6] == 'Checked-In':
                    print("Ticket already used.")
                    return
                parts[6] = 'Checked-In'
                print("Ticket verified. Entry allowed.")
                updated.append(','.join(parts) + "\n")
            else:
                updated.append(line)
    if not found:
        print("Invalid Ticket ID.")
    else:
        with open(get_path("tickets.txt"), "w") as f:
            f.writelines(updated)

def show_records():
    if not os.path.exists(get_path("bookings.txt")):
        print("No booking records found.")
        return
    with open(get_path("bookings.txt")) as f:
        for line in f:
            print(line.strip())


def add_event():
    eid = input("Enter Event ID: ").strip()
    name = input("Enter Event Name: ").strip()
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    venue = input("Enter Venue: ").strip()
    event = Event(eid, name, date, venue)
    while True:
        ttype = input("Enter Ticket Type: ").strip()
        price = float(input("Enter Price: "))
        quota = int(input("Enter Quota: "))
        event.add_ticket_type(ttype, price, quota)
        more = input("Add another ticket type? (y/n): ").strip().lower()
        if more != 'y':
            break
    save_event(event)
    print("Event and ticket types saved.")
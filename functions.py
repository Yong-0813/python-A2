# functions.py
import os
import random
from event import Event
from bill import Bill
import ticket
events_filename = "events.txt"
bookings_filename = "bookings.txt"
tickets_filename = "tickets.txt"

def functionMenu():
    return {
        "1": "Add New Event",
        "2": "Book Ticket",
        "3": "Check-In Ticket",
        "4": "Show All Bookings",
        "5": "Exit"
    }


def eventOptionMenu():
    event_dict = {}

    with open(events_filename, "r") as events:
        for event_info in events:
            info = event_info.strip().split(",")

            if len(info) >= 2:
                event_id = info[0]
                event_name = info[1]

                if event_id not in event_dict:
                    event_dict[event_id] = event_name
    return event_dict


def addEvent():
    print("\n=== Add New Event ===")
    
    exist_id = []
    with open(events_filename, "r") as info:
        for line in info:
            if line.strip():
                event_id = line.strip().split(",")[0]
                exist_id.append(event_id)

    while True:
        event_id = input("\nEnter Event ID (e.g. E001): ").strip()
        if event_id in exist_id:
            print("This Event ID already exists! Please enter a another unique Event ID.")
        else:
            break

    event_name = input("Please Enter Event Name: ").strip()
    event_date = input("Please Enter Event Date (YYYY-mm-dd): ").strip()
    event_venue = input("Please Enter Event Venue: ").strip()

    event_info = Event(event_id, event_name, event_date, event_venue)

    while True:
        ticket_type = input("\nPlease Enter Ticket Type (VIP, Student): ").strip()
        price = input("Please Enter Ticket Price (10.00): ").strip()
        quota = input("Please Enter Ticket Quota: ").strip()

        event_info.add_ticket_type(ticket_type, price, quota)

        addMore = input("Add another ticket type? (y/n): ").strip().lower()
        if addMore != 'y':
            break

    with open(events_filename, "a") as addInfo:
        addInfo.write(str(event_info) + "\n")

    print("\n" + "=" * 30)
    print(f"{event_info.name} added successfully!")
    print("=" * 30)


def bookTicket():
    print("\n=== Book Ticket ===")
    duplicate_id = []

    with open(events_filename, "r") as events_info:
        for info in events_info:
            if info.strip():
                info_parts = info.strip().split(",")
                event_id = info_parts[0]
                
                found = False
                for dup_event_id in duplicate_id:
                    if dup_event_id == event_id:
                        found = True
                        break

                if not found:
                    name = info_parts[1]
                    date = info_parts[2]
                    venue = info_parts[3]
                    print(f"{event_id} - {name} | {date} | {venue}\n")
                    duplicate_id.append(event_id)

    while True:
        selectID = input("Please Enter Event ID: ").strip()
        found = False
        for dup_event_id in duplicate_id:
            if selectID == dup_event_id:
                found = True
                break
        if not found:
            print("Invalid event ID! Please Enter Again!")
        else:
            break
    print("\n" + "=" * 30)
    print(f"Ticket Types for Event {selectID}")
    print("=" * 30 + "\n")
    tickets = {}

    with open(events_filename, "r") as ticket_info:
        for info in ticket_info:
            if info.strip():
                info_parts = info.strip().split(",")
                if info_parts[0] == selectID:
                    ticket_type = info_parts[4]
                    price = float(info_parts[5])
                    quota = int(info_parts[6])
                    tickets[ticket_type] = {"price": price, "quota": quota}
                    print(f"- {ticket_type}: RM{price:.2f} (Remaining: {quota})")

    while True:
        selectType = input("\nPlease Enter Ticket Type: ").strip()
        
        matched_type = None
        for type in tickets:
            if selectType.lower() == type.lower():
                matched_type = type
                break

        if not matched_type:
            print("Invalid Ticket Type! Please Enter Again!")
            continue

        ticketQuantity = input("How Many Tickets Needed: ").strip()

        if not ticketQuantity.isdigit():
            print("Please enter a valid number.")
            continue

        ticketQuantity = int(ticketQuantity)
        if ticketQuantity <= 0:
            print("Quantity must be at least 1.")
            continue

        if ticketQuantity > tickets[matched_type]["quota"]:
            print(f"Sorry, only {tickets[matched_type]['quota']} tickets available for {matched_type}.")
            continue

        tickets[matched_type]["quota"] -= ticketQuantity
        break
    
    lines = []
    with open(events_filename, "r") as event_info:
        for info in event_info:
            if info.strip():
                info_part = info.strip().split(",")
                if info_part[0] == selectID and info_part[4] == selectType:
                    info_part[6] = str(tickets[selectType]["quota"])
                    info = ",".join(info_part)
                lines.append(info)

    with open(events_filename, "w") as updateQuota:
        for info in lines:
            updateQuota.write(info + "\n")


    print("\n=== Customer Details ===")
    buyer_name = input("Please Enter Customer Name: ")
    ic_passport = input("Please Enter IC/Passport No: ")

    last_booking_id = 0
    with open(bookings_filename, "r") as booking_info:
        for info in booking_info:
            if info.strip():
                booking_id = info.strip().split(",")[0]
                if booking_id.startswith("B") and booking_id[1:].isdigit():
                    num = int(booking_id[1:])
                    if num > last_booking_id:
                        last_booking_id = num

    new_booking_id = "B" + str(last_booking_id + 1).zfill(4)

    existing_ticketID = []
    with open(tickets_filename, "r") as ticket_info:
        for info in ticket_info:
            if info.strip():
                ticket_id = info.strip().split(",")[0]
                existing_ticketID.append(ticket_id)
    
    new_ticket_id = []

    for _ in range(ticketQuantity):
        while True:
            random_digits = str(random.randint(100000, 999999))
            check_ticket_id = f"{selectID}-{random_digits}"
            exists = False
            for ticketID in existing_ticketID:
                if check_ticket_id == ticketID or check_ticket_id in new_ticket_id:
                    exists = True
                    break
            if not exists:
                new_ticket_id.append(check_ticket_id)
                break

    bill_info = Bill(new_booking_id)
    bill_info.subtotal = tickets[matched_type]["price"] * ticketQuantity
    for ticket_id in new_ticket_id:
        bill_info.add_ticket(ticket_id)

    event_name, event_date, event_venue = "", "", ""
    with open(events_filename, "r") as event_info:
        for info in event_info:
            if info.strip():
                info_parts = info.strip().split(",")
                if info_parts[0] == selectID:
                    event_name = info_parts[1]
                    event_date = info_parts[2]
                    event_venue = info_parts[3]
                    break

    bill_info.print_invoice(buyer_name, ic_passport, event_name, event_date, event_venue, tickets[matched_type]["price"], ticketQuantity, new_ticket_id , selectType) 

    # Save to bookings.txt
    with open(bookings_filename, "a") as booking_file:
        booking_file.write(f"{new_booking_id},{buyer_name},{ic_passport},{selectID},{event_name},{matched_type},{ticketQuantity},{bill_info.booking_date},{bill_info.total_charge():.2f}\n")

    # Save to tickets.txt
    with open(tickets_filename, "a") as ticket_file:
        for ticket_id in new_ticket_id: 
            ticket_file.write(f"{ticket_id},{new_booking_id},{selectID},{matched_type},{buyer_name},{ic_passport},{"Active"}\n")


def checkInTicket():
    print("\n=== Ticket Check-In ===")
    while True:
        ticket_id_input = input("\nPlease Enter Ticket ID: ").strip()

        found = False
        updated_lines = []

        with open(tickets_filename, "r") as ticket_info:
            for info in ticket_info:
                if info.strip():
                    info_parts = info.strip().split(",")
                    ticket_id = info_parts[0]
                    status = info_parts[-1] if len(info_parts) >= 5 else "Active"

                    if ticket_id == ticket_id_input:
                        found = True
                        if status.lower() == "checked-in":
                            print("Ticket already checked in.")
                        else:
                            print("Check-In Successful.")
                            info_parts[-1] = "Checked-In"
                        info = ",".join(info_parts)
                updated_lines.append(info.strip())

        if not found:
            print("Ticket ID not found.")

        else:
            with open(tickets_filename, "w") as file:
                for line in updated_lines:
                    file.write(line + "\n")
            break


def showRecords():
    print("\n=== Booking Summary ===\n")
    print("{:<12} {:<20} {:<20} {:<20} {:<10} {:<10} {:<18}".format("Book ID","Buyer Name","IC/Passport", "Event Name", "Type", "Quantity", "Total Price (RM)"))
    with open(bookings_filename, "r") as bookings_info:
        for info in bookings_info:
            if info.strip():
                info_parts = info.strip().split(",")
                if len(info_parts) < 9:
                    print("Error: Lose infomation of booking record!\n")
                    continue

                booking_id = info_parts[0]
                buyer_name = info_parts[1]
                ic_passport = info_parts[2]
                event_name = info_parts[4]
                ticket_type = info_parts[5]
                quantity = info_parts[6]
                total_charge = info_parts[8]

                print("{:<12} {:<20} {:<20} {:<20} {:<10} {:<10} {:<18}".format(booking_id, buyer_name,ic_passport, event_name, ticket_type, quantity, total_charge))

# functions.py
import os
import random
from datetime import datetime
from event import Event
from bill import Bill
from ticket import Ticket

# variable for each file
events_filename = "events.txt"
bookings_filename = "bookings.txt"
tickets_filename = "tickets.txt"

# ********************** Main Menu **********************
def functionMenu():
    return {
        "1": "Add New Event",
        "2": "Book Ticket",
        "3": "Check-In Ticket",
        "4": "Show All Bookings",
        "5": "Exit"
    }


# Event Option and List to display, used dict{} to prevent duplicate event_id
def eventOptionMenu():
    event_dict = {}

    with open(events_filename, "r") as events:
        for event_info in events:
            info = event_info.strip().split(",")

            if len(info) >= 4:
                event_id = info[0]
                event_name = info[1]
                event_date = info[2]
                event_venue = info [3]

                if event_id not in event_dict:
                    event_dict[event_id] = {
                        "name": event_name,
                        "date": event_date,
                        "venue": event_venue
                    }
    return event_dict

# ********************** Add Event Function **********************
def addEvent():
    print("\n=== Ongoing Event ===")
    # eventOptionMenu to show added event list
    event_dict = eventOptionMenu()
    for event_id, event_info in event_dict.items():
        name = event_info["name"]
        date = event_info["date"]
        venue = event_info["venue"]
        print(f"{event_id} - {name} | {date} | {venue}")

    print("\n=== Add New Event ===")
    
    event_name = input("Please Enter Event Name: ").strip() # Event Title
    if check_cancel(event_name):
        return
    
    while True:
        event_date = input("Please Enter Event Date (yyyyMMdd): ").strip() # Event Date
        # check validity of date input
        if check_cancel(event_date):
            return
        if not is_valid_date(event_date):
            print("Invalid date! Please enter a valid date in YYYYMMDD format.")
            continue
        break

    event_venue = input("Please Enter Event Venue: ").strip() # Event Venue
    if check_cancel(event_venue):
        return

    event_info = Event(event_name, event_date, event_venue)

    # a list to store added ticket types
    added_types = []
    while True:
        ticket_type = input("\nPlease Enter Ticket Type (VIP, Student): ").strip() # Ticket Type
        if check_cancel(ticket_type):
            return
        # to check duplicate input for ticket types
        if ticket_type.lower() in (t.lower() for t in added_types):
            print("This ticket type has already been added. Please enter a different type.")
            continue

        price = input("Please Enter Ticket Price (RM): ").strip() # Ticket Price
        if check_cancel(price):
            return
        quota = input("Please Enter Ticket Quota: ").strip() # Ticket Quota
        if check_cancel(quota):
            return

        event_info.add_ticket_type(ticket_type, price, quota)
        added_types.append(ticket_type) # append added ticket type into added_type list

        # add another ticket type
        addMore = input("Add another ticket type? (y/n): ").strip().lower()
        if check_cancel(addMore):
            return
        if addMore != 'y':
            break
    
    # write event info into events.txt
    with open(events_filename, "a") as addInfo:
        addInfo.write(str(event_info) + "\n")

    # display successful message
    print("\n" + "=" * 50)
    print(f"Event [{event_info.event_id}] - {event_info.name} added successfully!")
    print("=" * 50)

# ********************** Book Ticket Function **********************
def bookTicket():
    print(f"\n{'='*10} Book Ticket {'='*10}")
    
    # eventOptionMenu to show event list
    event_dict = eventOptionMenu()
    for event_id, event_info in event_dict.items():
        name = event_info["name"]
        date = event_info["date"]
        venue = event_info["venue"]
        print(f"\n{'Event ID':<12}: [ {event_id} ]\n{'Event Title':<12}: {name}\n{'Date':<12}: {date}\n{'Venue':<12}: {venue}\n")
        print("-"*33)

    while True:
        selectID = input("Please Enter Event ID: ").strip().upper() # Event ID input
        if check_cancel(selectID):
            return
        # use event_dict to validate event id entered by user
        if event_dict.get(selectID.upper()) is None:
            print("Invalid event ID! Please Enter Again!")
        else:
            break
    print("\n" + "=" * 30)
    print(f"Ticket Types for Event {selectID}")
    print("=" * 30 + "\n")
    tickets = {}

    # Display available ticket
    with open(events_filename, "r") as ticket_info:
        for info in ticket_info:
            if info.strip():
                info_parts = info.strip().split(",")
                if info_parts[0] == selectID:
                    ticket_type = info_parts[4]
                    price = float(info_parts[5])
                    quota = int(info_parts[6])
                    tickets[ticket_type] = {"price": price, "quota": quota}
                    print(f"{ticket_type.upper():<8}: RM{price:.2f} (Remaining: {quota})")
    # Check availability of ticket type
    while True:
        selectType = input("\nPlease Enter Ticket Type: ").strip() # Ticket Type input
        if check_cancel(selectType):
            return
        matched_type = None
        for type in tickets:
            if selectType.lower() == type.lower():
                matched_type = type
                break

        if not matched_type:
            print("Invalid Ticket Type! Please Enter Again!")
            continue

        ticketQuantity = input("How Many Tickets Needed: ").strip() # Ticket Quantity input
        if check_cancel(ticketQuantity):
            return
        # validate input
        if not ticketQuantity.isdigit():
            print("Please enter a valid number.")
            continue
        ticketQuantity = int(ticketQuantity)
        if ticketQuantity <= 0:
            print("Quantity must be at least 1.")
            continue

        # check enter quantity and available ticket
        if ticketQuantity > tickets[matched_type]["quota"]:
            print(f"Sorry, only {tickets[matched_type]['quota']} tickets available for {matched_type.upper()}.")
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

    # Customer Details
    print("\n=== Customer Details ===")
    buyer_name = input("Please Enter Customer Name: ") # Customer Name input
    if check_cancel(buyer_name):
        return
    ic_passport = input("Please Enter IC/Passport No: ") # Customer IC/Passport No input
    if check_cancel(ic_passport):
        return
    # Check latest Booking Id to prevent duplicate
    last_booking_id = 0
    with open(bookings_filename, "r") as booking_info:
        for info in booking_info:
            if info.strip():
                booking_id = info.strip().split(",")[0]
                if booking_id.startswith("B") and booking_id[1:].isdigit():
                    num = int(booking_id[1:])
                    if num > last_booking_id:
                        last_booking_id = num
    # assign new booking id
    new_booking_id = "B" + str(last_booking_id + 1).zfill(4) # Booking ID generate

    # list to store existing ticket ID to pevent duplicate
    existing_ticketID = []
    with open(tickets_filename, "r") as ticket_info:
        for info in ticket_info:
            if info.strip():
                ticket_id = info.strip().split(",")[0]
                existing_ticketID.append(ticket_id)
    
    new_ticket_id = []

    for _ in range(ticketQuantity):
        while True:
            random_digits = str(random.randint(100000, 999999)) # generate random digits for ticket id
            check_ticket_id = f"{selectID}-{random_digits}" # generate Ticket ID
            exists = False
            # check duplicate
            for ticketID in existing_ticketID:
                if check_ticket_id == ticketID or check_ticket_id in new_ticket_id:
                    exists = True
                    break
            if not exists:
                new_ticket_id.append(check_ticket_id)
                break
    
    # Pass input to Bill to generate bill
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
    
    # Print bill
    bill_info.print_invoice(buyer_name, ic_passport, event_name, event_date, event_venue, tickets[matched_type]["price"], ticketQuantity, new_ticket_id , selectType) 

    # Update file
    # update quota in event.txt
    with open(events_filename, "w") as updateQuota:
        for info in lines:
            updateQuota.write(info.strip() + "\n")

    # Save to bookings.txt
    with open(bookings_filename, "a") as booking_file:
        booking_file.write(f"{new_booking_id},{buyer_name},{ic_passport},{selectID},{event_name},{matched_type},{ticketQuantity},{bill_info.booking_date},{bill_info.total_charge():.2f}\n")

    # Save to tickets.txt using Ticket Class
    with open(tickets_filename, "a") as ticket_file:
        for ticket_id in new_ticket_id: 
            ticket = Ticket(
                ticket_id = ticket_id,
                booking_id = new_booking_id,
                event_id = selectID,
                ticket_type = matched_type,
                buyer_name = buyer_name,
                ic_number = ic_passport,
                
            )
            ticket_file.write(str(ticket))
# ********************** Check In Ticket Function **********************
def checkInTicket():
    print("\n=== Ticket Check-In ===")
    while True:
        ticket_id_input = input("\nPlease Enter Ticket ID: ").strip() # Ticket ID input

        found = False
        updated_lines = [] # store checked in ticket info

        # retrive ticket info
        with open(tickets_filename, "r") as ticket_info:
            for info in ticket_info:
                if info.strip():
                    info_parts = info.strip().split(",")
                    ticket_id = info_parts[0]
                    status = info_parts[-1] if len(info_parts) >= 5 else "Active"
                    
                    if ticket_id == ticket_id_input:
                        found = True
                        # Check ticket status
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
            # update ticket status
            with open(tickets_filename, "w") as file:
                for line in updated_lines:
                    file.write(line + "\n")
            break

# ********************** Show Records **********************
def showRecords():
    print("\n=== Booking Summary ===\n")
    print(f"{'-'*145}")
    print("{:<12} {:<30} {:<20} {:<30} {:<10} {:<10} {:<18}".format("Book ID","Buyer Name","IC/Passport", "Event Name", "Type", "Quantity", "Total Price (RM)"))
    print(f"{'-'*145}")
    with open(bookings_filename, "r") as bookings_info:
        for info in bookings_info:
            if info.strip():
                info_parts = info.strip().split(",")
                # to check any corrupted line
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

                print("{:<12} {:<30} {:<20} {:<30} {:<10} {:<10} {:<18}".format(booking_id, buyer_name,ic_passport, event_name, ticket_type.upper(), quantity, total_charge))

# cancel option for user to denied current session and back to menu
def check_cancel(input_str):
    if input_str.strip().lower() in ["cancel"]:
        print("\nAction cancelled. Returning to main menu...\n")
        return True
    return False

# check validity of date
def is_valid_date(date_str):
    if len(date_str) != 8 or not date_str.isdigit():
        return False
    try:
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False


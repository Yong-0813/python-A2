# Directory structure:
# - main.py
# - event.py
# - ticket.py
# - bill.py
# - functions.py
# - events.txt
# - bookings.txt
# - tickets.txt

# main.py
from functions import *

def main():
    while True:
        menu = functionMenu()
        print("\nWelcome to INTI Event Ticketing System")
        for k, v in menu.items():
            print(f"{k}. {v}")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_event()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            check_in_ticket()
        elif choice == '4':
            show_records()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
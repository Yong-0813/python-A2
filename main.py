# main.py
from functions import *

while True:
    menu = functionMenu()
    print("\nWelcome to INTI Event Ticketing System")
    for k, v in menu.items():
        print(f"{k}. {v}")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        addEvent()
    elif choice == '2':
        bookTicket()
    elif choice == '3':
        checkInTicket()
    elif choice == '4':
        showRecords()
    elif choice == '5':
        print("Thank You!")
        break
    else:
        print("Invalid option. Try again.")